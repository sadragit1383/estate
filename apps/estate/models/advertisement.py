# apps/estate/models/advertisement.py

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from .base import SlugBaseModel
from apps.core.models.location_model import Area, City
from apps.user.models.user_model import User
from apps.user.models.validation.user_validation import CleanFieldsMixin


def get_expiry_date():
    return timezone.now() + timedelta(days=30)


class AdvertisementType(SlugBaseModel):
    class Meta:
        verbose_name = 'نوع آگهی'
        verbose_name_plural = 'انواع آگهی'


class PropertyType(SlugBaseModel):
    advertisement_types = models.ManyToManyField(
        AdvertisementType,
        related_name='property_types',
        verbose_name='نوع آگهی'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children', verbose_name='والد'
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


class Advertisement(SlugBaseModel, CleanFieldsMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements', verbose_name='کاربر آگهی‌دهنده')
    userConfirm = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_advertisements', verbose_name='کاربر تأیید‌کننده')
    advType = models.ForeignKey(AdvertisementType, on_delete=models.CASCADE, related_name='advertisements', verbose_name='نوع آگهی')
    propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='advertisements', verbose_name='نوع ملک')
    premiumtypes = models.ManyToManyField(TypePremium, blank=True, verbose_name='نوع پرمیوم')
    status = models.ForeignKey(StatusAdvertisemen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='وضعیت')
    description = models.TextField(verbose_name='توضیحات')
    price = models.BigIntegerField(verbose_name='قیمت آگهی')
    viewCount = models.BigIntegerField(default=0, verbose_name='تعداد بازدید')
    expired_at = models.DateTimeField(default=get_expiry_date, verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی‌ها'

    def clean(self):
        if self.expired_at < timezone.now():
            raise ValidationError("تاریخ انقضا نمی‌تواند در گذشته باشد.")

    @property
    def is_expired(self):
        return self.expired_at < timezone.now()


class AdvertisementLocation(models.Model):
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True, verbose_name='آگهی')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='محله')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر')


class SecretAdvertisement(models.Model):
    advertisement = models.OneToOneField(Advertisement, on_delete=models.CASCADE, primary_key=True, verbose_name='آگهی')
    isRenewal = models.BooleanField(default=False, verbose_name='تمدید')
    isInfoCompleted = models.BooleanField(default=False, verbose_name='تکمیل اطلاعات')
    isFlagged = models.BooleanField(default=False, verbose_name='وضعیت آگهی مشکوک')




