from django.db import models
from users.models import User


class Tag(models.Model):
    name_tag = models.CharField()
    color = ...
    slug = models.SlugField()


class Ingridient(models.Model):
    name_ingridient = models.CharField()
    amount = models.FloatField()
    unit = models.CharField()


class Recipe(models.Model):
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False
    )
    name = models.CharField(
        'Название',
        blank=False
    )
    image = models.ImageField(
        blank=False
    )
    description = models.CharField(
        blank=False
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False
    )
    time_cook = models.DateTimeField(
        blank=False
    )