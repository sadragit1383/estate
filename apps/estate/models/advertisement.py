from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .base import SlugBaseModel
from apps.core.models.location_model import Area,City
from apps.user.models.validation.user_validation import CleanFieldsMixin
from apps.user.models.user_model import User
from datetime import timedelta
from apps.estate.models.utilities import get_expiry_date

class AdvertisementType(SlugBaseModel):
    class Meta:
        verbose_name = 'نوع آگهی'
        verbose_name_plural = 'انواع آگهی'


class PropertyType(SlugBaseModel):

    advertisement_types = models.ManyToManyField(
        AdvertisementType,
        verbose_name='نوع آگهی',
        related_name='property_types'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='والد',
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name = 'نوع ملک'
        verbose_name_plural = 'انواع ملک'


class StatusAdvertisemen(SlugBaseModel):
    class Meta:
        verbose_name = 'وضعیت آگهی'
        verbose_name_plural = 'وضعیت‌های آگهی'


class TypePremium(SlugBaseModel):
    class Meta:
        verbose_name = 'نوع خاص'
        verbose_name_plural = 'پرمیوم‌ها'



def get_expiry_date():

    return timezone.now() + timedelta(days=30)



class Advertisement(SlugBaseModel,CleanFieldsMixin):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='کاربر آگهی‌دهنده',
        related_name='advertisements'
    )

    userConfirm = models.ForeignKey(
         User,
        on_delete=models.SET_NULL,
        verbose_name='کاربر تأیید‌کننده',
        related_name='confirmed_advertisements',
        null=True,
        blank=True
    )

    advType = models.ForeignKey(
        AdvertisementType,
        on_delete=models.CASCADE,
        verbose_name='نوع آگهی',
        related_name='advertisements'
    )

    propertyType = models.ForeignKey(
        PropertyType,
        on_delete=models.CASCADE,
        verbose_name='نوع ملک',
        related_name='advertisements'
    )

    premiumtypes = models.ManyToManyField(
        TypePremium,
        verbose_name='نوع پرمیوم',
        blank=True
    )

    status = models.ForeignKey(
        StatusAdvertisemen,
        on_delete=models.SET_NULL,
        verbose_name='وضعیت',
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name='توضیحات',

    )



    price = models.BigIntegerField(verbose_name='قیمت آگهی')
    viewCount = models.BigIntegerField(default=0, verbose_name='تعداد بازدید')

    expired_at = models.DateTimeField(
        verbose_name='تاریخ انقضا',
        default = get_expiry_date
    )



    class Meta:
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی‌ها'


    def clean(self):
        if self.expired_at < timezone.now():
            raise ValidationError("تاریخ انقضا نمی‌تواند در گذشته باشد.")


    @property
    def is_expired(self):
        """بررسی انقضای آگهی"""
        return self.expired_at < timezone.now()


class AdvertisementLocation(models.Model):

    advertisement = models.OneToOneField(Advertisement,on_delete=models.CASCADE,verbose_name='اگهی',primary_key=True)
    area = models.ForeignKey(Area,on_delete=models.CASCADE,verbose_name='محله')
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name='شهر')


class SecretAdvertisement(models.Model):

    advertisement = models.OneToOneField(Advertisement,on_delete=models.CASCADE,verbose_name='اگهی',primary_key=True)
    isRenewal = models.BooleanField(default=False, verbose_name='تمدید')
    isInfoCompleted = models.BooleanField(default=False, verbose_name='تکمیل اطلاعات')
    isFlagged = models.BooleanField(default=False, verbose_name='وضعیت اگهی مشکوک')