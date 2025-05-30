from django.db import models
import utils
from apps.user.models.user_model import User,banUsers
from apps.core.models.location_model import Province, City
from apps.user.models.meta.meta_class import DynamicFieldMeta
from apps.user.models.validation.user_validation import CleanFieldsMixin
from .validation.agency_valid import *
from django.http import JsonResponse
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
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

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

    profileImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[profile_image_validator],)
    bannerImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[profile_image_validator],)
    logoImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[profile_image_validator],)
    licenceImage = models.ImageField(upload_to=agency_uploader.upload_to, null=True, blank=True,validators=[profile_image_validator],)

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

    def deactivate_member(self, user_id):



        from .requestagency_model import RequestCollaborationAgency, StatusResponse

        updated = False

        # غیرفعال‌سازی اگر مشاور بود
        consultant_qs = self.consultants.filter(user_id=user_id, isActive=True)
        if consultant_qs.exists():
            consultant_qs.update(isActive=False)
            updated = True

        # غیرفعال‌سازی اگر مدیر بود
        manager_qs = self.managers.filter(user_id=user_id, isActive=True)
        if manager_qs.exists():
            manager_qs.update(isActive=False)
            updated = True

        if not updated:
            raise ValidationError("کاربر فعال با این آژانس یافت نشد.")

        # لغو درخواست‌های همکاری مرتبط با آژانس و کاربر
        RequestCollaborationAgency.objects.filter(
            agency=self,
            user_id=user_id,
            status=StatusResponse.ACCEPTED,
            isActive=True
        ).update(
            status=StatusResponse.CANCELLED,
            isActive=False,
            responseMessage="درخواست به دلیل غیرفعال‌سازی از سوی آژانس لغو شد."
        )



    @classmethod
    def confirm_agency(cls, agency_id):

        try:
            agency = cls.objects.get(pk=agency_id)

            if agency.status == cls.Status.ACTIVE:
                return False, "این آژانس قبلاً تایید شده است"

            # تایید آژانس
            agency.status = cls.Status.ACTIVE
            agency.save()

            # تغییر نقش کاربر به agency
            from apps.user.models.user_model import RoleUser
            agency_role, _ = RoleUser.objects.get_or_create(
                slug='agency',
                defaults={'title': 'Agency', 'isActive': True}
            )
            agency.user.role = agency_role
            agency.user.save()

            return True, "آژانس با موفقیت تایید شد"

        except cls.DoesNotExist:
            return False, "آژانس با این شناسه یافت نشد"
        except Exception as e:
            return False, f"خطا در تایید آژانس: {str(e)}"

    # ================== Staff Base ==================

class StaffBase(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(upload_to=profile_uploader.upload_to, null=True, blank=True,validators=[profile_image_validator],)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='%(class)ss')
    isActive = models.BooleanField(default=False,verbose_name='وضعیت فعال')

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


class RejectedAgency(TimestampedModel):

    agency = models.ForeignKey(Agency,verbose_name='اژآنس',blank=True,null=True,on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن پیام',blank=True,null=True)


    def __str__(self):
        return f'{self.text}'


