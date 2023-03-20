import re

from django.core.exceptions import ValidationError


def validate_username(value):
    allowed = r'^[\w.@+-]+\Z'
    if not re.match(allowed, value):
        raise ValidationError(
            "(Имя пользователя может содержать только буквы,)"
            "(цифры и знаки '_', '@', '+', '.', '-'.)"
        )


def validate_username_me(username):
    if username == "me":
        raise ValidationError(
            'Невозможно создать пользователя с таким именем!'
        )
