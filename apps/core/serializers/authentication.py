# core/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        # بررسی اینکه کاربر OTP را تایید کرده است
        if not hasattr(user, 'usersecret') or not user.usersecret.isVerfied:
            raise AuthenticationFailed('User not verified with OTP')

        return user