import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import utils
from django.core.exceptions import ValidationError
from .meta.meta_class import DynamicFieldMeta
from .validation.user_validation import CleanFieldsMixin, ValidMobileNumber, PasswordValidator
from .abstract_model import AbstractBaseModel
from .user_mixin import UserMethodsMixin
from rest_framework import status
from ..response_handler import ResponseHandler
from .user_model import User



class UserStatusChoices(models.TextChoices):
    ENTERED = 'entered', 'ورود'
    ACTIVE = 'active', 'داخل سایت'
    EXITED = 'exited', 'خروج'


class UserUseage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    startTime = models.DateTimeField(default=timezone.now, verbose_name='زمان شروع')
    endTime = models.DateTimeField(verbose_name='زمان اتمام پروژه', null=True, blank=True)
    result = models.CharField(max_length=100, verbose_name='نتیجه ماندگاری', blank=True)
    status = models.CharField(max_length=10, choices=UserStatusChoices.choices, verbose_name='وضعیت')



    def save(self, *args, **kwargs):
        if self.status == UserStatusChoices.EXITED and self.endTime and self.startTime:
            delta = self.endTime - self.startTime
            minutes, seconds = divmod(delta.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            self.result = f"{int(hours)} ساعت، {int(minutes)} دقیقه، {int(seconds)} ثانیه"
        super().save(*args, **kwargs)
