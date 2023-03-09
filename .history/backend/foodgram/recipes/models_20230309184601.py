from django.db import models
from users.models import User


class Tag(models.Model):
    name_tag = models.CharField(
        unique=True,
        blank=False,
        help_text='Введи тег',
    )
    color = ...
    slug = models.SlugField(
        unique=True,
        blank=False,
    )


class Ingridient(models.Model):
    name_ingridient = models.CharField(
        blank=False,
    )
    amount = models.FloatField(
        blank=False,
        help_text='Введите число',
    )
    unit = models.CharField(
        blank=False,
        help_text='Введите единицу измерения',
    )


class Recipe(models.Model):
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        help_text='Введите Ваше имя',
    )
    name = models.CharField(
        'Название',
        blank=False,
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        blank=False
    )
    description = models.CharField(
        blank=False,
        help_text='Придумайте описание',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        blank=False,
        help_text='Выберите ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        help_text='Выберите теги'
    )
    time_cook = models.DateTimeField(
        blank=False,
        help_text='Выберите время приготовления',
    )