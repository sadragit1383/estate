def get_model_fields(model_instance, fields_to_extract, context=None):


    result = {}
    request = context.get('request') if context else None

    for field in fields_to_extract:
        # اگر فیلد یک متد باشد (مثل get_images)
        if hasattr(model_instance, f'get_{field}'):
            method = getattr(model_instance, f'get_{field}')
            result[field] = method()

        # اگر فیلد یک رابطه (ForeignKey, OneToOne) باشد
        elif '__' in field:
            related_fields = field.split('__')
            value = model_instance
            for related_field in related_fields:
                value = getattr(value, related_field, None)
                if value is None:
                    break
            result[field] = str(value) if value else None

        else:
            value = getattr(model_instance, field, None)

            if hasattr(value, 'url') and request:
                result[field] = request.build_absolute_uri(value.url)
            else:
                result[field] = str(value) if value else None

    return result