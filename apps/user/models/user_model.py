""" User Management Module """
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import utils
from django.core.exceptions import ValidationError
from .meta.meta_class import DynamicFieldMeta
from .validation.user_validation import CleanFieldsMixin, ValidMobileNumber, PasswordValidator
from .abstract_model import AbstractBaseModel


def validate_password(value):
    validator = PasswordValidator()
    validator(value)


class UserValidator:
    """Validator class for User-related validations."""
    @staticmethod
    def validate_mobile_number(mobile_number):
        """
        Validate if a given mobile number matches required format.
        Raises ValueError if validation fails.
        """
        if not mobile_number:
            raise ValueError("پارامتر شماره موبایل الزامی است.")
        try:
            ValidMobileNumber(mobile_number)
        except ValidationError as exc:
            raise ValueError(f"شماره موبایل نامعتبر است: {str(exc)}")

    @staticmethod
    def validate_password(password):
        """
        Validate if a given password matches requirements.
        Raises ValueError if validation fails.
        """
        if not password:
            raise ValueError("رمز عبور الزامی است.")
        try:
            PasswordValidator(password)
        except ValidationError as exc:
            raise ValueError(f"رمز عبور نامعتبر است: {str(exc)}")


class UserManager(BaseUserManager):
    """
    Custom User Manager to handle creation and validation of users and superusers.
    """



    def get_user(self, mobile_number):
        """
        Returns user instance for the given mobile number.
        Raises ValueError if user not found.
        """
        try:
            return self.model.objects.get(mobileNumber=mobile_number)
        except self.model.DoesNotExist:
            raise ValueError("کاربری با این شماره موبایل یافت نشد.")


    def create_user(self, mobile_number, password=None, **extra_fields):
        """
        Creates a regular user with given mobile number and optional password.
        """
        UserValidator.validate_mobile_number(mobile_number)
        if password:
            UserValidator.validate_password(password)

        user = self.model(mobileNumber=mobile_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        """
        Creates a superuser with given mobile number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validate required fields
        for field in self.model.REQUIRED_FIELDS:
            if field not in extra_fields:
                raise ValueError(f'فیلد {field} برای سوپر یوزر ضروری است.')

        return self.create_user(mobile_number, password, **extra_fields)

    def check_user(self, mobile_number):
        """
        Checks if a user with the given mobile number exists.
        """
        return self.model.objects.filter(mobileNumber=mobile_number).exists()

    def create_user_secret(self, user):
        active_code = utils.create_random_code(5)  # تولید کد ۵ رقمی
        expire_date = timezone.now() + timezone.timedelta(minutes=2)  # انقضای ۵ دقیقه‌‌ای

        user_secret, created = UserSecret.objects.update_or_create(
            user=user,
            defaults={
                "activeCode": active_code,
                "expireDate": expire_date,
                "isBan": False,
                "isVerfied": False,
                "isInfoFiled": False,
                "isActive": True
            }
        )
        return user_secret

    def verify_user_secret(self, user, code):
        try:
            user_secret = UserSecret.objects.get(user=user)
            if user_secret.activeCode == code and user_secret.expireDate >= timezone.now():
                user_secret.isVerfied = True
                user_secret.isActive = True
                user_secret.save()
                return user_secret
            else:
                raise ValueError("کد نامعتبر یا منقضی شده است.")
        except UserSecret.DoesNotExist:
            raise ValueError("اطلاعات تایید کاربر یافت نشد.")


class Gender(models.TextChoices):
    """Gender Choices"""
    MALE = 'male', 'مرد'
    FEMALE = 'femail', 'زن'
    OTHER = 'other', 'سایر'


class RoleUser(models.Model):
    """Role User Model"""
    id = models.UUIDField(primary_key=True, verbose_name='ایدی', editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=20, verbose_name='عنوان')
    slug = models.CharField(max_length=20, verbose_name='نامک نقش')
    isActive = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        db_table = 'user_role'
        app_label = 'user'


class User(AbstractBaseUser, PermissionsMixin, CleanFieldsMixin, metaclass=DynamicFieldMeta):
    """
    Custom User Model
    """
    __dynamic_blank_fields__ = ['firstName', 'lastName', 'email', 'countryCode',
                              'gender', 'createAt', 'birthday', 'role', 'password']

    # Required fields for custom user model
    USERNAME_FIELD = 'mobileNumber'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    objects = UserManager()

    id = models.UUIDField(
        primary_key=True, verbose_name='ایدی', editable=False, default=uuid.uuid4
    )
    mobileNumber = models.CharField(
        unique=True, max_length=11, verbose_name='شماره موبایل', validators=[ValidMobileNumber]
    )
    firstName = models.CharField(max_length=50, verbose_name='نام کوچیک')
    lastName = models.CharField(max_length=100, verbose_name='نام فامیلی')
    email = models.EmailField(verbose_name='ایمیل', max_length=100)
    countryCode = models.CharField(max_length=5, verbose_name='کد کشور')
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.MALE, verbose_name="جنسیت"
    )
    birthday = models.CharField(max_length=20, verbose_name='تاریخ تولد')
    role = models.ForeignKey(RoleUser, verbose_name='نقش کاربر', on_delete=models.CASCADE)
    password = models.CharField(
        max_length=128,
        verbose_name='رمز عبور',
        validators=[validate_password]
    )
    is_superuser = models.BooleanField(default=False, verbose_name='کاربر ادمین پلاس')


    class Meta:
        db_table = 'user'
        app_label = 'user'


    def get_full_name(self):
        """
        Returns full name of the user.
        If firstName and lastName are empty, returns mobileNumber as fallback.
        """
        full_name = f"{self.firstName or ''} {self.lastName or ''}".strip()
        if not full_name:
            return  "کاربر"
        return full_name


    def is_admin(self):
        """
        Checks if the user is an admin or superuser.
        """
        return self.role.slug == 'admin' or self.is_superuser

    def set_password(self, raw_password):
        """
        Hashes and sets the password for the user.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def activate_user_info(self):
        """
        Activates user info if linked to UserSecret model.
        """
        if hasattr(self, 'usersecret'):
            self.usersecret.isInfoFiled = True
            self.usersecret.isActive = True
            self.usersecret.save()

    def deactivate(self):
        """
        Deactivates the user account if linked to UserSecret model.
        """
        if hasattr(self, 'usersecret'):
            self.usersecret.isActive = False
            self.usersecret.save()



class UserSecret(AbstractBaseModel, models.Model):
    """User Secret Model"""
    user = models.OneToOneField(User, verbose_name='کاربر', on_delete=models.CASCADE)
    isBan = models.BooleanField(default=False, verbose_name='وضعیت بلاک')
    isVerfied  = models.BooleanField(default=False)
    isInfoFiled = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    activeCode = models.CharField(max_length=5, verbose_name='کد تایید')
    expireDate = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انقضا')

    class Meta:
        db_table = 'user_secret'
        app_label = 'user'


class UserLogin(models.Model):
    """User Login Model"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='کاربر'
    )
    lastLogin = models.DateTimeField(
        auto_now_add=True, verbose_name='زمان اخرین ورود'
    )
    ip = models.CharField(max_length=15, verbose_name='ای پی')  # محدودیت طول IP اضافه شد

    class Meta:
        db_table = 'user_login'
        app_label = 'user'