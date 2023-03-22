from django.core.exceptions import ValidationError


def validate_username_me(username):
    if username.lower() == "me":
        raise ValidationError(
            'Невозможно создать пользователя с таким именем!'
        )
