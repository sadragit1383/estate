import ipaddress
from django.http import HttpRequest
from django.db import models
from ..models.loguser_model import User, UserLog

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        # ثبت تمام خطاهای با کد وضعیت 400 به بالا
        if response.status_code >= 400:
            self.log_error(request, response)

        return response

    def log_error(self, request: HttpRequest, response):
        user = request.user if request.user.is_authenticated else None
        ip_address = self.get_client_ip(request)
        endpoint = request.path
        error_code = str(response.status_code)

        # دریافت پیام خطا
        error_message = getattr(response, 'reason_phrase', None)
        if not error_message:
            try:
                error_message = str(response.content)[:500]
            except:
                error_message = "Unknown error"

        # ایجاد یا به‌روزرسانی لاگ خطا
        try:
            if user:
                # برای کاربران لاگین شده
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
                    log.count = models.F('count') + 1
                    log.message = error_message
                    log.save()
            else:
                # برای کاربران ناشناس (بر اساس IP)
                log, created = UserLog.objects.get_or_create(
                    ipAddress=ip_address,
                    code=error_code,
                    endpoint=endpoint,
                    defaults={
                        'message': error_message,
                        'count': 1
                    }
                )
                if not created:
                    log.count = models.F('count') + 1
                    log.message = error_message
                    log.save()
        except Exception as e:
            # در صورت بروز خطا در ثبت لاگ
            print(f"Error logging failed: {e}")

    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORAD_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')

        # اعتبارسنجی IP
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            return 'invalid_ip'