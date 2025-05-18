from django.db import models
from .user_model import User
from django.utils import timezone
from datetime import timedelta

# تابع کمکی برای محاسبه زمان انقضا
def default_expire_time():
    return timezone.now() + timedelta(days=3)

class UserLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        blank=True,
        null=True
    )
    code = models.CharField(
        max_length=5,
        verbose_name='کد خطا'
    )
    endpoint = models.CharField(
        max_length=255,
        verbose_name='آدرس اندپوینت'
    )
    message = models.TextField(
        verbose_name='تکست خطا',
        blank=True,
        null=True
    )
    count = models.PositiveIntegerField(
        verbose_name='تعداد دفعات',
        default=0
    )
    ipAddress = models.CharField(
        max_length=1000,
        verbose_name='آدرس IP',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'user_log'
        app_label = 'user'

    def __str__(self):
        return f'{self.user} - {self.code}'


class BlockedIP(models.Model):

    ip_address = models.GenericIPAddressField(unique=True, verbose_name='آدرس IP')
    blocked_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان بلاک')
    reason = models.TextField(blank=True, null=True, verbose_name='دلیل بلاک')
    requests_count = models.PositiveIntegerField(default=1, verbose_name='تعداد درخواست‌ها')
    time_frame_seconds = models.PositiveIntegerField(verbose_name='بازه زمانی (ثانیه)',blank=True,null=True)
    max_requests = models.PositiveIntegerField(verbose_name='حداکثر درخواست مجاز',blank=True,null=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'IP بلاک شده'
        verbose_name_plural = 'IPهای بلاک شده'
        ordering = ['-blocked_at']

    def __str__(self):
        return f"{self.ip_address} (بلاک شده در {self.blocked_at})"

    def is_block_expired(self):
        """بررسی انقضای زمان بلاک"""
        expiration_time = self.blocked_at + timezone.timedelta(seconds=self.time_frame_seconds)
        return timezone.now() > expiration_time




class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['ip_address', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"





