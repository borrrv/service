from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
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
        null=True,
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
    USERNAME_FIELD = ['email',]
    REQUIRED_FIELDS = ['email', 'id', 'username', 'first_name', 'last_name']
        
    def __str__(self):
        return self.username