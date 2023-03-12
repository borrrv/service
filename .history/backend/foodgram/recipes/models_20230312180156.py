from django.db import models
from users.models import User
from django.core.validators import RegexValidator


class Tag(models.Model):
    name_tag = models.CharField(
        unique=True,
        blank=False,
        help_text='Введи тег',
        max_length=200,
    )
    color = models.CharField(
        max_length=7,
        validators=[RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")],
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        max_length=200,
    )

    def __str__(self):
        return self.name_tag



class Ingredient(models.Model):
    name = models.CharField(
        blank=False,
        max_length=50,
        help_text='Укажите название ингридиента',
    )
    amount = models.FloatField(
        blank=False,
        null=True,
        help_text='Введите количество',
    )
    unit = models.CharField(
        blank=False,
        help_text='Введите единицу измерения',
        max_length=30,
    )

    def __str__(self):
        return f'{self.name}, {self.unit}'


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
        max_length=30,
    )
    image = models.ImageField(
        blank=False,
        upload_to='static/images/'
    )
    text = models.CharField(
        blank=False,
        help_text='Придумайте описание',
        max_length=100,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        help_text='Выберите ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        help_text='Выберите теги'
    )
    cooking_time = models.IntegerField(
        blank=False,
        help_text='Выберите время приготовления',
    )


class IngredientReciepe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    reciepes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        help_text='Введите количество продукта'
    )

    def __str__(self):
        return f'{self.ingredients}, {self.value}'