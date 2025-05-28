from django.core.exceptions import ValidationError
import re
import os

def validate_name(value):
    """
    Validator for name field that checks:
    - Length between 3 and 25 characters
    - Doesn't contain any digits (English or Persian)
    """
    # Check length
    if len(value) < 3:
        raise ValidationError('نام باید حداقل 3 کاراکتر باشد.')
    if len(value) > 25:
        raise ValidationError('نام نمی‌تواند بیشتر از 25 کاراکتر باشد.')

    # Check for any digits (English 0-9 or Persian ۰-۹)
    if re.search(r'[\d۰-۹]', value):
        raise ValidationError('نام نمی‌تواند شامل عدد باشد.')


from django.core.exceptions import ValidationError
import re
import os

def validate_name(value):
    """
    Validator for name field that checks:
    - Length between 3 and 25 characters
    - Doesn't contain any digits (English or Persian)
    """
    # Check length
    if len(value) < 3:
        raise ValidationError('نام باید حداقل 3 کاراکتر باشد.')
    if len(value) > 25:
        raise ValidationError('نام نمی‌تواند بیشتر از 25 کاراکتر باشد.')

    # Check for any digits (English 0-9 or Persian ۰-۹)
    if re.search(r'[\d۰-۹]', value):
        raise ValidationError('نام نمی‌تواند شامل عدد باشد.')

def simple_image_validator(value, max_size_kb=400, allowed_extensions=None):
    """
    اعتبارسنجی ساده برای تصاویر

    پارامترهای پیش‌فرض:
        max_size_kb=400 (حداکثر حجم به کیلوبایت)
        allowed_extensions=['png'] (لیست فرمت‌های مجاز)
    """
    if allowed_extensions is None:
        allowed_extensions = ['png']

    # بررسی حجم
    if value.size > max_size_kb * 1024:  # تبدیل به بایت
        raise ValidationError(f'حجم تصویر باید کمتر از {max_size_kb} کیلوبایت باشد.')

    # بررسی پسوند
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'فقط فرمت‌های {", ".join(allowed_extensions)} مجاز هستند.')

# توابع اعتبارسنجی از پیش تعریف شده برای استفاده در مدل‌ها
def default_image_validator(value):
    """اعتبارسنجی پیش‌فرض برای تصاویر (400KB, PNG)"""
    return simple_image_validator(value, max_size_kb=400, allowed_extensions=['png'])

def profile_image_validator(value):
    """اعتبارسنجی مخصوص تصاویر پروفایل (500KB, PNG/JPG)"""
    return simple_image_validator(value, max_size_kb=500, allowed_extensions=['png', 'jpg', 'jpeg'])

def large_image_validator(value):
    """اعتبارسنجی برای تصاویر بزرگتر (1MB, PNG/JPG)"""
    return simple_image_validator(value, max_size_kb=1024, allowed_extensions=['png', 'jpg', 'jpeg'])