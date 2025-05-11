from django.db import models


class DynamicFieldMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        blankable_fields = attrs.get('__dynamic_blank_fields__', [])
        new_class = super().__new__(cls, name, bases, attrs)

        for field_name in blankable_fields:
            try:
                field = new_class._meta.get_field(field_name)
                field.blank = True
                field.null = True
            except Exception:
                pass

        return new_class
