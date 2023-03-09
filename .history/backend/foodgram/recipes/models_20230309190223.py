from django.db import models
from users.models import User


class Tag(models.Model):
    name_tag = models.CharField(
        unique=True,
        blank=False,
        help_text='Введи тег',
    )
    color = models.CharField(
        max_length=20,
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
    )

    def __str__(self):
        return self.name_tag


class Ingridient(models.Model):
    name_ingridient = models.CharField(
        blank=False,
        max_length=50,
        help_text='Укажите название ингридиента',
    )
    amount = models.FloatField(
        blank=False,
        help_text='Введите количество',
    )
    unit = models.CharField(
        blank=False,
        help_text='Введите единицу измерения',
    )

    def __str__(self):
        return f'{self.name_ingridient}, {self.unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        help_text='Введите имя автора рецепта',
    )
    name = models.CharField(
        'Название',
        blank=False,
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        blank=False,
        upload_to='static/images/'
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


class IngridientReciepe(models.Model):
    ingridients = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
    )
    reciepes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        help_text='Введите количество продукта'
    )