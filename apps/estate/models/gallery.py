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
    thumbnail_image = models.ImageField(upload_to=upload_thumbnail, verbose_name='تصویر بند انگشتی', blank=True, null=True)
    small_image = models.ImageField(upload_to=upload_small, verbose_name='تصویر کوچک', blank=True, null=True)
    medium_image = models.ImageField(upload_to=upload_medium, verbose_name='تصویر متوسط', blank=True, null=True)
    large_image = models.ImageField(upload_to=upload_large, verbose_name='تصویر بزرگ', blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_org = models.BooleanField(default=False, verbose_name='عکس شاخص')
    slug = models.CharField(max_length=50, verbose_name='اسلاگ', blank=True, null=True)


    class Meta:
        verbose_name = 'گالری آگهی'
        verbose_name_plural = 'گالری‌های آگهی'

    def __str__(self):
        return f"{self.advertisement.title} - تصویر"

    def resize_and_save_new_image(self, source_image_path, destination_path, width, height):
        """Resize and save image to the given path."""
        try:
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            img = Image.open(source_image_path)
            img_format = img.format if img.format else 'JPEG'
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail((width, height), Image.LANCZOS)
            img.save(destination_path, format=img_format, quality=95, optimize=True)
            return destination_path
        except Exception as e:
            print(f"خطا در تغییر اندازه تصویر: {e}")
            return None

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if not self.org_image:
            return

        original_image_path = self.org_image.path
        if not os.path.exists(original_image_path):
            print(f"تصویر اصلی یافت نشد: {original_image_path}")
            return

        updates = []

        def process_variant(field_name, upload_func, width, height):
            nonlocal updates
            if getattr(self, field_name):
                return
            path = os.path.join(settings.MEDIA_ROOT, upload_func(self, f"{self.id}.jpg"))
            resized_path = self.resize_and_save_new_image(original_image_path, path, width, height)
            if resized_path:
                setattr(self, field_name, os.path.relpath(resized_path, settings.MEDIA_ROOT))
                updates.append(field_name)

        process_variant("thumbnail_image", upload_thumbnail, 192, 108)
        process_variant("small_image", upload_small, 320, 170)
        process_variant("medium_image", upload_medium, 768, 480)
        process_variant("large_image", upload_large, 1280, 768)

        if updates:
            super().save(update_fields=updates + ["is_active", "is_org", "slug"])
