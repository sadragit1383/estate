from django.http import HttpRequest
from django.utils import timezone
from ..models.user_log import UserLog,User
import ipaddress

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        if 500 <= response.status_code < 600:
            self.log_error(request, response)

        return response

    def log_error(self, request: HttpRequest, response):
        # استخراج اطلاعات کاربر
        user = request.user if request.user.is_authenticated else None
        ip_address = self.get_client_ip(request)
        endpoint = request.path
        error_code = str(response.status_code)
        error_message = getattr(response, 'reason_phrase', '') or str(response.content)[:500]

        # اگر کاربر لاگین کرده باشد
        if user:
            log, created = UserLog.objects.get_or_create(
                user=user,
                code=error_code,
                endpoint=endpoint,
                defaults={
                    'message': error_message,
                    'count': 1
                }
            )
            if not created:
                log.count += 1
                log.message = error_message
                log.save()
        else:

            anonymous_user, _ = User.objects.get_or_create(
                username=f'anonymous_{ip_address}',
                defaults={
                    'firstName': 'Anonymous',
                    'lastName': ip_address,
                    'is_active': False
                }
            )
            log, created = UserLog.objects.get_or_create(
                user=anonymous_user,
                code=error_code,
                endpoint=endpoint,
                defaults={
                    'message': error_message,
                    'count': 1
                }
            )
            if not created:
                log.count += 1
                log.message = error_message
                log.save()

    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # اعتبارسنجی IP آدرس
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            return 'invalid_ip'