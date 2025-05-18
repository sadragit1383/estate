from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models.user_model import User, RoleUser, UserSecret, UserLogin
from .models.wallet_model import Currency, Wallet
from apps.user.models.loguser_model import UserLog, BlockedIP, RequestLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """مدیریت حرفه‌ای کاربر در پنل ادمین"""

    list_display = ('mobileNumber', 'firstName', 'lastName', 'email', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'gender', 'role')
    search_fields = ('mobileNumber', 'firstName', 'lastName', 'email')
    ordering = ('-id',)
    readonly_fields = ('id',)

    fieldsets = (
        (_('اطلاعات کاربری'), {
            'fields': (
                'mobileNumber', 'password',
                'firstName', 'lastName', 'email',
                'countryCode', 'gender', 'birthday', 'role'
            )
        }),
        (_('دسترسی‌ها'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (_('ساخت کاربر جدید'), {
            'classes': ('wide',),
            'fields': (
                'mobileNumber', 'password1', 'password2',
                'firstName', 'lastName', 'email',
                'gender', 'role',
                'is_staff', 'is_superuser'
            ),
        }),
    )


@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    """مدیریت نقش‌ها"""
    list_display = ('title', 'slug', 'isActive')
    search_fields = ('title', 'slug')
    list_filter = ('isActive',)


@admin.register(UserSecret)
class UserSecretAdmin(admin.ModelAdmin):
    """مدیریت کد فعال‌سازی کاربران"""
    list_display = ('user', 'activeCode', 'expireDate', 'isVerfied', 'isBan', 'isActive')
    search_fields = ('user__mobileNumber', 'activeCode')
    list_filter = ('isVerfied', 'isBan', 'isActive')
    readonly_fields = ('expireDate',)


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    """مدیریت لاگ‌های ورود کاربران"""
    list_display = ('user', 'lastLogin', 'ip')
    search_fields = ('user__mobileNumber', 'ip')
    readonly_fields = ('lastLogin',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """مدیریت ارزها"""
    list_display = ('name', 'symbol', 'isActive', 'createAt', 'updateAt')
    search_fields = ('name', 'symbol')
    list_filter = ('isActive',)
    readonly_fields = ('uuid', 'createAt', 'updateAt')
    ordering = ('-createAt',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """مدیریت کیف‌پول کاربران"""
    list_display = ('user', 'currency', 'balance', 'isActive', 'createAt')
    search_fields = ('user__mobileNumber', 'user__firstName', 'user__lastName')
    list_filter = ('isActive', 'currency')
    readonly_fields = ('uuid', 'createAt')
    ordering = ('-createAt',)




@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'endpoint', 'count', 'ipAddress')
    search_fields = ('user__username', 'code', 'endpoint', 'ipAddress')
    list_filter = ('code',)
    readonly_fields = ('user', 'code', 'endpoint', 'message', 'ipAddress', 'count')
    ordering = ('-count',)

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked_at', 'is_active', 'requests_count', 'max_requests', 'time_frame_seconds')
    search_fields = ('ip_address',)
    list_filter = ('is_active',)
    readonly_fields = ('blocked_at',)
    ordering = ('-blocked_at',)

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp')
    search_fields = ('ip_address',)
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)