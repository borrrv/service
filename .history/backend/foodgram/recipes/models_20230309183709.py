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
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Название'
    )
    image = models.ImageField()
    description = models.CharField()
    ingridients = models.ManyToManyField(Ingridient)
    tags = models.ManyToManyField(Tag)
    time_cook = models.TimeField()