import os
import uuid
from PIL import Image
from django.conf import settings
from django.db import models


# ------------------ Upload Path Functions ------------------

def upload_original(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery/original/", filename)

def upload_thumbnail(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery/xs/", filename)

def upload_small(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery/sm/", filename)

def upload_medium(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery/md/", filename)

def upload_large(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery/lg/", filename)

# ------------------ AdvertisementGallery Model ------------------


class AdvertisementGallery(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    advertisement = models.ForeignKey(
        'Advertisement', on_delete=models.CASCADE,
        related_name='advertisement_gallery',
        verbose_name='آگهی'
    )

    org_image = models.ImageField(upload_to=upload_original, verbose_name='تصویر اصلی', blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to=upload_thumbnail, blank=True, null=True)
    small_image = models.ImageField(upload_to=upload_small, blank=True, null=True)
    medium_image = models.ImageField(upload_to=upload_medium, blank=True, null=True)
    large_image = models.ImageField(upload_to=upload_large, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_org = models.BooleanField(default=False)
    slug = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'گالری آگهی'
        verbose_name_plural = 'گالری‌های آگهی'

    def __str__(self):
        return f"{self.advertisement.title} - تصویر"
