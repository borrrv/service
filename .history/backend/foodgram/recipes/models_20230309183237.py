from django.db import models
from users.models import User

class Recipe(models.Model):
    username = models.ForeignKey(
        
    )
    name = models.CharField(
        'Название'
    )
    image = models.ImageField()
    description = models.CharField()
    ingridients = models.ManyToManyField()
    tags = models.ManyToManyField()
    time_cook = models.TimeField()


class Tag(models.Model):
    name_tag = models.CharField()
    color = 
    slug = models.SlugField()


class Ingridient(models.Model):
    name_ingridient = models.CharField()
    amount = models.FloatField()
    unit = models.CharField()