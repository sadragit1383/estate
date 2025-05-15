from django.db import models

class DynamicFieldMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        blankable_fields = getattr(new_class, '__dynamic_blank_fields__', [])

        for field_name in blankable_fields:
            try:
                field = new_class._meta.get_field(field_name)

                # فقط فیلدهای قابل ویرایش را تغییر بده
                if isinstance(field, (models.CharField, models.TextField, models.EmailField, models.DateTimeField, models.DateField, models.IntegerField, models.FloatField, models.BooleanField, models.ForeignKey)):
                    field.blank = True
                    field.null = True
            except Exception as e:
                continue

        return new_class
