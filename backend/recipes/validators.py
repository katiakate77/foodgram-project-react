from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Время приготовления должно быть больше либо равно 1 мин'
        )
    return value
