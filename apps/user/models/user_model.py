from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid


class Gender(models.TextChoices):

    MALE = 'male','مرد'
    FEMALE = 'femail','زن'
    OTHER = 'other','سایر'


class RoleUser(models.Model):

    id = models.UUIDField(primary_key=True,verbose_name='ایدی',editable=False,default=uuid.uuid4())
    title = models.CharField(max_length=20,verbose_name='عنوان')
    slug = models.CharField(max_length=20,verbose_name='نامک نقش')


class User(models.Model):

    id = models.UUIDField(primary_key=True,verbose_name='ایدی',editable=False,default=uuid.uuid4())
    mobileNumber = models.CharField(unique=True,max_length=11,verbose_name='شماره موبایل',)
    firstName = models.CharField(max_length=50,verbose_name='نام کوچیک')
    lastName = models.CharField(max_length=100,verbose_name='نام فامیلی')
    email = models.EmailField(verbose_name='ایمیل',max_length=100)
    countryCode = models.CharField(max_length=5,verbose_name='کد کشور')
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.MALE,
        blank=True,
        null=True,
        verbose_name="جنسیت",
    )
    createAt = models.DateTimeField(auto_now_add=True)
    birthday = models.CharField(max_length=20,verbose_name='تاریخ تولد')
    role = models.ForeignKey(RoleUser,verbose_name='نقش کاربر')
    password = models.CharField(max_length=36,verbose_name='رمز عبور')


class UserSecret(models.Model):

    userId = models.OneToOneField(User,verbose_name='کاربر')
    isBan = models.BooleanField(default=False,verbose_name='وضعیت بلاک')
    isVerfied = models.BooleanField(default=False)
    isInfoFiled = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    expireDate = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انقضا')

