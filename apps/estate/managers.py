from django.db import models
from django.utils import timezone

class AdvertisementManager(models.Manager):
    """مدیر سفارشی برای مدل Advertisement"""

    def active(self):

        return self.get_queryset().filter(
            is_active=True,
            expired_at__gte=timezone.now()
        )

    def premium(self):
        """آگهی‌های پرمیوم"""
        return self.active().filter(
            premium_types__isnull=False
        ).distinct()

    def by_user(self, user):
        """آگهی‌های یک کاربر خاص"""
        return self.filter(user=user)

    def by_property_type(self, property_type):
        """آگهی‌های یک نوع ملک خاص"""
        return self.active().filter(property_type=property_type)


class GalleryManager(models.Manager):
    """مدیر سفارشی برای مدل AdvertisementGallery"""

    def primary_images(self):
        """تصاویر شاخص"""
        return self.filter(is_primary=True)

    def by_advertisement(self, advertisement):
        """تصاویر یک آگهی خاص"""
        return self.filter(advertisement=advertisement).order_by('-is_primary')