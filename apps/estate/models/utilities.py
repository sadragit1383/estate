import os
from django.conf import settings
from ..validators import validate_future_date, validate_image_size, validate_price
from PIL import Image
from django.utils import timezone
from datetime import timedelta


def upload_to_adv_gallery(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "images", filename)


class ImageResizer:


    @staticmethod
    def resize_image(image, width, height):
        """تغییر اندازه تصویر با حفظ نسبت ابعاد"""
        img = image.copy()
        img.thumbnail((width, height), Image.LANCZOS)
        return img

    @staticmethod
    def save_image(image, path, format='JPEG', quality=90):
        """ذخیره تصویر در مسیر مشخص"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image.save(path, format=format, quality=quality, optimize=True)


def get_expiry_date():
    return timezone.now() + timedelta(days=30)

def upload_to_original(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "original", filename)

def upload_to_thumbnail(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "thumbnail", filename)

def upload_to_small(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "small", filename)

def upload_to_medium(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "medium", filename)

def upload_to_large(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("advertisement_gallery", "large", filename)
