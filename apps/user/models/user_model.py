from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from .meta.meta_class import DynamicFieldMeta
from .validation.user_validation import CleanFieldsMixin,ValidMobileNumber
from .abstract_model import AbstractBaseModel
import uuid


class UserManager(BaseUserManager):

    def create_user(self, mobileNumber, password=None, **extra_fields):
        if not mobileNumber:
            raise ValueError("شماره موبایل الزامی است.")

        user = self.model(mobileNumber=mobileNumber, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  
        user.save(using=self._db)
        return user


    def create_superuser(self, mobileNumber, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError("رمز عبور برای سوپر یوزر الزامی است.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("سوپر یوزر باید is_superuser=True داشته باشد.")

        return self.create_user(mobileNumber, password, **extra_fields)



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


class User(AbstractBaseModel, models.Model, CleanFieldsMixin, metaclass=DynamicFieldMeta):

    __dynamic_blank_fields__ = ['firstName', 'lastName', 'email', 'countryCode', 'gender', 'createAt', 'birthday', 'role', 'password']

    id = models.UUIDField(primary_key=True, verbose_name='ایدی', editable=False, default=uuid.uuid4())
    mobileNumber = models.CharField(unique=True, max_length=11, verbose_name='شماره موبایل', validators=[ValidMobileNumber])
    firstName = models.CharField(max_length=50, verbose_name='نام کوچیک')
    lastName = models.CharField(max_length=100, verbose_name='نام فامیلی')
    email = models.EmailField(verbose_name='ایمیل', max_length=100)
    countryCode = models.CharField(max_length=5, verbose_name='کد کشور')
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name="جنسیت",
    )
    birthday = models.CharField(max_length=20, verbose_name='تاریخ تولد')
    role = models.ForeignKey(RoleUser, verbose_name='نقش کاربر')
    password = models.CharField(max_length=36, verbose_name='رمز عبور')
    is_superuser = models.BooleanField(default=False, verbose_name='کاربر ادمین پلاس')

    class Meta:
        db_table = 'user'
        app_label = 'userapp'


    def get_full_name(self):
        return f"{self.firstName} {self.lastName}".strip()


    def is_admin(self):
        return self.role.slug == 'admin' or self.is_superuser


    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)


    def activate_user_info(self):
        if hasattr(self, 'usersecret'):
            self.usersecret.isInfoFiled = True
            self.usersecret.isActive = True
            self.usersecret.save()


    def deactivate(self):
        if hasattr(self, 'usersecret'):
            self.usersecret.isActive = False
            self.usersecret.save()


    class Meta:
        db_table = 'user'
        app_label = 'userapp'


class UserSecret(AbstractBaseModel,models.Model):

    user = models.OneToOneField(User,verbose_name='کاربر')
    isBan = models.BooleanField(default=False,verbose_name='وضعیت بلاک')
    isVerfied = models.BooleanField(default=False)
    isInfoFiled = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    activeCode = models.CharField(max_length=5,verbose_name='کد تایید')
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