from django.db import models

class Recipe(models.Model):
    username = models.ForeignKey()
    name = models.CharField()
    image = models.ImageField()
    description = models.CharField()
    ingridient = models.ManyToManyField()
    tag = models.ManyToManyField()
    time_cook = models.TimeField()