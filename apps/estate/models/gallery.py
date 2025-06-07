import os
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .base import BaseModel
from .utilities import (
    upload_to_original,
    upload_to_thumbnail,
    upload_to_small,
    upload_to_medium,
    upload_to_large
)

class AdvertisementGallery(BaseModel):
    advertisement = models.ForeignKey(
        'Advertisement',
        on_delete=models.CASCADE,
        verbose_name='آگهی',
        related_name='gallery'
    )

    original_image = models.ImageField(
        upload_to=upload_to_original,
        verbose_name='تصویر اصلی'
    )

    thumbnail = models.ImageField(
        upload_to=upload_to_thumbnail,
        verbose_name='تصویر بند انگشتی',
        blank=True
    )

    small = models.ImageField(
        upload_to=upload_to_small,
        verbose_name='تصویر کوچک',
        blank=True
    )

    medium = models.ImageField(
        upload_to=upload_to_medium,
        verbose_name='تصویر متوسط',
        blank=True
    )

    large = models.ImageField(
        upload_to=upload_to_large,
        verbose_name='تصویر بزرگ',
        blank=True
    )


    class Meta:
        verbose_name = 'گالری آگهی'
        verbose_name_plural = 'گالری‌های آگهی'

    def save(self, *args, **kwargs):
        if not self.pk and self.original_image:
            # برای تصاویر جدید، نسخه‌های مختلف ایجاد می‌کنیم
            super().save(*args, **kwargs)
            self.create_image_variations()
        else:
            super().save(*args, **kwargs)

    def create_image_variations(self):
        """ایجاد نسخه‌های مختلف از تصویر اصلی"""
        if not self.original_image:
            return

        image = Image.open(self.original_image)
        image_format = image.format if image.format else 'JPEG'

        # تبدیل به RGB اگر تصویر RGBA است
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')

        # ایجاد نسخه‌های مختلف
        sizes = {
            'thumbnail': (192, 108),
            'small': (320, 170),
            'medium': (768, 480),
            'large': (1280, 768)
        }

        for size_name, dimensions in sizes.items():
            self.resize_and_save_image(image, size_name, dimensions, image_format)


    def resize_and_save_image(self, original_image, size_name, dimensions, image_format):
        """تغییر اندازه تصویر و ذخیره آن"""
        resized_image = original_image.copy()
        resized_image.thumbnail(dimensions, Image.LANCZOS)

        buffer = BytesIO()
        resized_image.save(buffer, format=image_format, quality=90)
        buffer.seek(0)

        file_name = os.path.basename(self.original_image.name)
        file_path = f"{size_name}/{file_name}"

        # ذخیره فایل
        file_field = getattr(self, size_name)
        file_field.save(file_path, ContentFile(buffer.read()), save=False)
        buffer.close()

        # ذخیره مدل بدون فراخوانی دوباره متد save
        super().save(update_fields=[size_name])