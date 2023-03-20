from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.settings import MAX_LENGTH

from .validators import validate_username, validate_username_me


class User(AbstractUser):
    """Модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

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
        max_length=MAX_LENGTH,
        help_text='Введите уникальный логин',
        validators=[validate_username_me, validate_username]
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH,
        blank=False,
        help_text='Введи вашем Имя',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH,
        blank=False,
        help_text='Введите вашу фамилию',
    )
    is_subscribed = models.BooleanField(
        'Подписка',
        default=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
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

    def __str__(self):
        return f'{self.user} : {self.author}'
