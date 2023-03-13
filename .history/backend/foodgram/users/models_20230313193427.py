from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Модель пользователя"""
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (GUEST, 'guest'),
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        blank=False,
        max_length=154,
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
    is_subscribed = models.BooleanField(
        'Подписка',
        default=False,
    )
    role = models.CharField(
        choices=ROLES,
        default=GUEST,
        max_length=10,
    )

    @property
    def is_guest(self):
        return self.role == self.GUEST
    
    @property
    def is_user(self):
        return self.role == self.USER
    
    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username}, {self.email}'