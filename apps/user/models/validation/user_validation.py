import re
from django.core.exceptions import ValidationError
from django.db import models

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





def ValidMobileNumber(value):

    if not re.fullmatch(r'^9\d{9}$', value):
        raise ValidationError("شماره موبایل باید ۱۰ رقم و بدون صفر ابتدایی باشد (مثلاً: 9123456789).")