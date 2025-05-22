from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .token_service import AbstractTokenService

class JWTTokenService(AbstractTokenService):
    def generate_access_token(self, user):
        return str(AccessToken.for_user(user))

    def generate_refresh_token(self, user):
        return str(RefreshToken.for_user(user))

    def refresh_token(self, refresh_token):
        refresh = RefreshToken(refresh_token)
        return str(refresh.access_token)