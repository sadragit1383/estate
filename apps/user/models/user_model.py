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
from .user_mixin import UserMethodsMixin
from rest_framework import status
from ..response_handler import ResponseHandler


def validate_password(value):
    validator = PasswordValidator()
    validator(value)


class UserValidator:
    """Validator class for User-related validations."""
    @staticmethod
    def validate_mobileNumber(mobileNumber):
        """
        Validate if a given mobile number matches required format.
        Raises ValueError if validation fails.
        """
        if not mobileNumber:
            raise ValueError("پارامتر شماره موبایل الزامی است.")
        try:
            ValidMobileNumber(mobileNumber)
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
            # The PasswordValidator class needs to be callable with the password directly
            # or have a method like .validate(password). Assuming it's callable.
            # If it expects an instance to be called, then `validator = PasswordValidator()` then `validator(password)`.
            # Based on `validate_password` function, it's callable.
            PasswordValidator()(password) # Call the instance
        except ValidationError as exc:
            raise ValueError(f"رمز عبور نامعتبر است: {str(exc)}")



class UserManager(BaseUserManager):
    """
    Custom User Manager to handle creation and validation of users and superusers.
    """


    def get_user(self, mobileNumber):
        """
        Returns user instance for the given mobile number.
        Raises ValueError if user not found.
        """
        try:
            return self.model.objects.get(mobileNumber=mobileNumber)
        except self.model.DoesNotExist:
            raise ValueError("کاربری با این شماره موبایل یافت نشد.")


    def create_user(self, mobileNumber, password=None, **extra_fields):
        """
        Creates a regular user with given mobile number and optional password.
        """
        UserValidator.validate_mobileNumber(mobileNumber)
        if password:
            UserValidator.validate_password(password)

        user = self.model(mobileNumber=mobileNumber, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user



    def create_superuser(self, mobileNumber, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given mobile number and password.
        """
        # Validate mobile number and password
        UserValidator.validate_mobileNumber(mobileNumber)
        if password:
            UserValidator.validate_password(password)

        # Set superuser defaults
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)  # Important for admin access

        # Ensure required fields are set
        extra_fields.setdefault('firstName', 'Admin')
        extra_fields.setdefault('lastName', 'User')
        extra_fields.setdefault('email', f'{mobileNumber}@admin.com')

        # Get or create the admin role
        role, created = RoleUser.objects.get_or_create(
            slug='admin',
            defaults={
                'title': 'Administrator',
                'isActive': True
            }
        )
        extra_fields['role'] = role

        # Create the user - let Django handle the ID generation
        user = self.model(
            mobileNumber=mobileNumber,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user


    def check_user(self, mobileNumber):
        """
        Checks if a user with the given mobile number exists.
        """
        return self.model.objects.filter(mobileNumber=mobileNumber).exists()



    def verify_user_otp(self, mobileNumber, active_code):
        """
        High-level OTP verification method
        Returns tuple: (user: User, error_message: str, status_code: int)
        """
        try:
            user = self.get(mobileNumber=mobileNumber)
            user_secret = UserSecret.objects.get(user=user)

            is_valid, message, code = user_secret.verify_otp(active_code)
            if not is_valid:
                return None, message, code

            user_secret.user.activate_user_info()
            return user, message, code

        except User.DoesNotExist:
            return None, "User with this mobile number not found.", status.HTTP_404_NOT_FOUND
        except UserSecret.DoesNotExist:
            return None, "OTP verification record not found.", status.HTTP_404_NOT_FOUND



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


    def loginAdmin(self, mobileNumber, password):
        """
        Authenticates an admin user with the given mobile number and password.
        Returns True on successful login, or a ResponseHandler.error on failure.
        """
        # 1. Basic input validation
        if not mobileNumber or not password:
            return ResponseHandler.error(
                code=status.HTTP_400_BAD_REQUEST,
                message='شماره موبایل و رمز عبور الزامی هستند.',
            )

        try:
            user = self.get(mobileNumber=mobileNumber)
        except self.model.DoesNotExist:
            return ResponseHandler.error(
                code=status.HTTP_404_NOT_FOUND,
                message='کاربر مورد نظر در سیستم موجود نیست.',
            )

        if not user.is_staff and not user.is_superuser:
            return ResponseHandler.error(
                code=status.HTTP_403_FORBIDDEN,  
                message='شما اجازه دسترسی به پنل مدیریت را ندارید.',
            )

        if not user.check_password(password):
            return ResponseHandler.error(
                code=status.HTTP_400_BAD_REQUEST,
                message='رمز عبور اشتباه است.',

            )

        return True


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


class User(AbstractBaseUser, PermissionsMixin, CleanFieldsMixin,UserMethodsMixin,metaclass=DynamicFieldMeta):
    """
    Custom User Model
    """
    __dynamic_blank_fields__ = ['firstName', 'lastName', 'email', 'countryCode',
                                  'gender', 'createAt', 'birthday', 'role', 'password']

    USERNAME_FIELD = 'mobileNumber'
    REQUIRED_FIELDS = ['firstName', 'lastName',]

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
    is_staff = models.BooleanField(default=False, verbose_name='کاربر ادمین ')


    class Meta:
        db_table = 'user'
        app_label = 'user'


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


    def verify_otp(self, active_code):
        """
        Verify the OTP code against this user secret
        Returns tuple: (is_valid: bool, error_message: str, status_code: int)
        """
        if self.isBan:
            return False, "User is banned from verification.", status.HTTP_403_FORBIDDEN

        if self.expireDate < timezone.now():
            return False, "OTP code has expired.", status.HTTP_410_GONE

        if self.activeCode != active_code:
            return False, "Invalid OTP code.", status.HTTP_403_FORBIDDEN


        return True, "OTP verified successfully.", status.HTTP_200_OK


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