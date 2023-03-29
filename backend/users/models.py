from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username_me


class User(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        blank=False,
        max_length=settings.MAX_LENGTH_EMAIL,
        help_text='Введите вашу электронную почту',
    )
    username = models.CharField(
        'Логин',
        unique=True,
        max_length=settings.MAX_LENGTH,
        help_text='Введите уникальный логин',
        validators=[validate_username_me,
                    UnicodeUsernameValidator]
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH,
        blank=False,
        help_text='Введи вашем Имя',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH,
        blank=False,
        help_text='Введите вашу фамилию',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username}, {self.email}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_user_and_author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_subscribe'
            )
        ]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} : {self.author}'
