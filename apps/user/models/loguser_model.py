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

class BlackList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )
    isBan = models.BooleanField(
        default=False,
        verbose_name='بلاک شده'
    )
    createAt = models.DateTimeField(
        default=timezone.now,
        verbose_name='ساخته شده'
    )
    ipAddress = models.CharField(
        max_length=1000,
        verbose_name='آدرس IP'
    )
    expireSince = models.DateTimeField(
        default=default_expire_time,
        verbose_name='تاریخ انقضا'
    )

    class Meta:
        db_table = 'black_list'
        app_label = 'user'

    def __str__(self):
        return f'{self.user} - {"بلاک شده" if self.isBan else "فعال"}'