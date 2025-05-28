from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdmin(permissions.BasePermission):
    """فقط برای کاربران با is_staff=True"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(permissions.BasePermission):
    """فقط برای کاربران با is_superuser=True"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)




class IsAgencyOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role.slug == 'agency'
        )