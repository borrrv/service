from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта'
        unique=True,
        blank=False,
        max_length=254,
    )
    username = models.CharField(
        'Логин',
        unique=True,
        null=True,
        max_length=150
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        blank=False,
    )
    def __str__(self):
        return self.username