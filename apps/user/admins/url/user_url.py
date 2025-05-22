# urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..view.useradmin_view import UserViewSet, RoleUserViewSet, UserSecretViewSet, UserLoginViewSet

admin_router = DefaultRouter()
admin_router.register(r'users', UserViewSet, basename='admin-users')
admin_router.register(r'roles', RoleUserViewSet, basename='admin-roles')
admin_router.register(r'secrets', UserSecretViewSet, basename='admin-secrets')
admin_router.register(r'logins', UserLoginViewSet, basename='admin-logins')

urlpatterns = [
    path('api/admin/', include(admin_router.urls)),
]
