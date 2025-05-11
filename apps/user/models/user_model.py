from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from .meta.meta_class import DynamicFieldMeta
from .validation.user_validation import CleanFieldsMixin,ValidMobileNumber
import uuid

class Gender(models.TextChoices):

    MALE = 'male','مرد'
    FEMALE = 'femail','زن'
    OTHER = 'other','سایر'


class RoleUser(models.Model):

    id = models.UUIDField(primary_key=True,verbose_name='ایدی',editable=False,default=uuid.uuid4())
    title = models.CharField(max_length=20,verbose_name='عنوان')
    slug = models.CharField(max_length=20,verbose_name='نامک نقش')

    class Meta:
        db_table = 'user_role'
        app_lable = 'userapp'


class User(models.Model,CleanFieldsMixin,metaclass = DynamicFieldMeta):

    __dynamic_blank_fields__ = ['firstName', 'lastName','email','countryCode','gender','createAt','birthday','role','password']

    id = models.UUIDField(primary_key=True,verbose_name='ایدی',editable=False,default=uuid.uuid4())
    mobileNumber = models.CharField(unique=True,max_length=11,verbose_name='شماره موبایل', validators=[ValidMobileNumber])
    firstName = models.CharField(max_length=50,verbose_name='نام کوچیک')
    lastName = models.CharField(max_length=100,verbose_name='نام فامیلی')
    email = models.EmailField(verbose_name='ایمیل',max_length=100)
    countryCode = models.CharField(max_length=5,verbose_name='کد کشور')
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name="جنسیت",
    )
    createAt = models.DateTimeField(auto_now_add=True)
    birthday = models.CharField(max_length=20,verbose_name='تاریخ تولد')
    role = models.ForeignKey(RoleUser,verbose_name='نقش کاربر')
    password = models.CharField(max_length=36,verbose_name='رمز عبور')
    is_superuser = models.BooleanField(default=False,verbose_name='کاربر ادمین پلاس')


    class Meta:
        db_table = 'user'
        app_label = 'userapp'


class UserSecret(models.Model):

    userId = models.OneToOneField(User,verbose_name='کاربر')
    isBan = models.BooleanField(default=False,verbose_name='وضعیت بلاک')
    isVerfied = models.BooleanField(default=False)
    isInfoFiled = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    expireDate = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انقضا')


    class Meta:
        db_table = 'user_secret'
        app_label = 'userapp'


class UserLogin(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر')
    lastLogin = models.DateTimeField(auto_now_add=True,verbose_name='زمان اخرین ورود')
    ip = models.CharField(verbose_name='ای پی')


    class Meta:
        db_table = 'user_login'
        app_label = 'userapp'