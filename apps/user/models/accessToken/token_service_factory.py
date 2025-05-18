# core/services/token_service_factory.py
from django.conf import settings
from .jwt_token_service import JWTTokenService

class TokenServiceFactory:
    @staticmethod
    def get_service():
        if settings.AUTH_SERVICE == 'jwt':
            return JWTTokenService()
        # امکان اضافه کردن سرویس‌های دیگر مانند OAuth
        raise ValueError("Unsupported token service")