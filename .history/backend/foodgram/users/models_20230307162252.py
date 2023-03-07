from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        blank=False,
        max_length=254,
        help_text='Введите вашу электронную почту',
    )
    username = models.CharField(
        'Логин',
        unique=True,
        max_length=150,
        help_text='Введите уникальный логин',
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        blank=False,
        help_text='Введи вашем Имя',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        blank=False,
        help_text='Введите вашу фамилию',
    )
        
    def __str__(self):
        return self.username