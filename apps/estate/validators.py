from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future_date(value):
    """اعتبارسنجی تاریخ آینده"""
    if value < timezone.now():
        raise ValidationError("تاریخ نمی‌تواند در گذشته باشد.")


def validate_image_size(image):
    """اعتبارسنجی اندازه تصویر"""
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError("حجم تصویر نمی‌تواند بیشتر از ۵ مگابایت باشد.")


def validate_price(value):
    """اعتبارسنجی قیمت"""
    if value < 0:
        raise ValidationError("قیمت نمی‌تواند منفی باشد.")