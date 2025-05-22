from rest_framework import viewsets, permissions
from ...models.user_model import User, RoleUser, UserSecret, UserLogin
from ..serializers.user_serializers import (
    UserSerializer, RoleUserSerializer, UserSecretSerializer, UserLoginSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class RoleUserViewSet(viewsets.ModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserSecretViewSet(viewsets.ModelViewSet):
    queryset = UserSecret.objects.all().select_related('user')
    serializer_class = UserSecretSerializer
    permission_classes = [permissions.IsAdminUser]


class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = UserLogin.objects.all().select_related('user')
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.IsAdminUser]