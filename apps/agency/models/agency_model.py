from django.db import models
import utils
from apps.user.models.user_model import User,banUsers
from apps.core.models.location_model import Province, City
from apps.user.models.meta.meta_class import DynamicFieldMeta
from apps.user.models.validation.user_validation import CleanFieldsMixin
from .validation.agency_valid import validate_name,simple_image_validator,create_image_validator

# ================== Ban Section ==================

class SubjectBan(models.TextChoices):
    AGENCY = 'agency', 'آژانس'
    CONSULTANT = 'consultant', 'مشاور'
    MANAGER = 'manager', 'مدیر'


# ================ Uploaders =======================

agency_uploader = utils.FileUpload('agency', 'images')
profile_uploader = utils.FileUpload('profile', 'avatars')


# ================ Shared Timestamp Model =======================

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ================== Agency Model ==================

class Agency(CleanFieldsMixin,TimestampedModel,metaclass=DynamicFieldMeta):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'فعال'
        INACTIVE = 'inactive', 'غیرفعال'
        REJECTED = 'rejected', 'رد شده'

    __dynamic_blank_fields__ = ['timeWork', 'bio', 'email', 'banner_image', 'bannerImage', 'logoImage']

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255,validators=[validate_name])

    profileImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[create_image_validator(400,['png','jpg'])])
    bannerImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[create_image_validator(400,['png','jpg'])])
    logoImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[create_image_validator(400,['png','jpg'])])
    licenceImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[create_image_validator(400,['png','jpg'])])

    email = models.EmailField(verbose_name='ایمیل املاک', blank=True, null=True)
    address = models.TextField(verbose_name='آدرس')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="استان")
    cities = models.ManyToManyField(City, blank=True, related_name='agencies')
    bio = models.TextField(null=True, blank=True)
    timeWork = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE
    )

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

    def reject_agency(self, reason: str):
        """
        رد کردن آژانس و ثبت آن در جدول banUsers
        """
        from apps.user.models.user_model import banUsers, SubjectBan

        self.status = self.Status.REJECTED
        self.save()

        banUsers.objects.create(
            user=self.user,
            text=reason,
            banSubject=SubjectBan.AGENCY
        )


# ================== Staff Base ==================

class StaffBase(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(upload_to=profile_uploader.upload_to, null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True


# ================== Consultant ==================

class Consultant(StaffBase):
    class Meta:
        verbose_name = "Consultant"
        verbose_name_plural = "Consultants"

    def __str__(self):
        return f'Consultant: {self.user}'


# ================== Manager ==================

class Manager(StaffBase):
    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def __str__(self):
        return f'Manager: {self.user}'
