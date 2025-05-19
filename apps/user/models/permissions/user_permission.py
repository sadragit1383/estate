from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """فقط برای کاربران با is_staff=True"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(permissions.BasePermission):
    """فقط برای کاربران با is_superuser=True"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)