import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _



def ValidMobileNumber(value):

    if not re.fullmatch(r'^9\d{9}$', value):
        raise ValidationError("شماره موبایل باید ۱۰ رقم و بدون صفر ابتدایی باشد (مثلاً: 9123456789).")


class CleanFieldsMixin:

    def clean(self):
        super().clean()
        for field in self._meta.fields:
            value = getattr(self, field.name)

            if isinstance(field, (models.CharField, models.TextField)):
                if value:
                    # Strip dangerous patterns (rudimentary SQLi protection)
                    if re.search(r"(;|--|\b(SELECT|INSERT|DELETE|DROP|UPDATE|EXEC|UNION)\b)", value, re.IGNORECASE):
                        raise ValidationError({field.name: "ورودی غیرمجاز است."})

                    # You may also strip HTML tags, emojis, etc., if needed
                    setattr(self, field.name, value.strip())

                    
class PasswordValidator:

    def __init__(self, min_length=8, require_upper=True, require_lower=True, require_digit=True, require_special=True, disallow_whitespace=True):

        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special
        self.disallow_whitespace = disallow_whitespace

    def __call__(self, password):
        errors = []

        if len(password) < self.min_length:
            errors.append(_("رمز عبور باید حداقل %(min)d کاراکتر باشد.") % {'min': self.min_length})

        if self.require_upper and not re.search(r'[A-Z]', password):
            errors.append(_("رمز عبور باید حداقل یک حرف بزرگ انگلیسی داشته باشد."))

        if self.require_lower and not re.search(r'[a-z]', password):
            errors.append(_("رمز عبور باید حداقل یک حرف کوچک انگلیسی داشته باشد."))

        if self.require_digit and not re.search(r'\d', password):
            errors.append(_("رمز عبور باید حداقل یک عدد داشته باشد."))

        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(_("رمز عبور باید حداقل یک کاراکتر خاص (مثل @ یا #) داشته باشد."))

        if self.disallow_whitespace and re.search(r'\s', password):
            errors.append(_("رمز عبور نباید شامل فاصله باشد."))

        if errors:
            raise ValidationError(errors)