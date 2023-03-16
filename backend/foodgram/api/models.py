from django.core.validators import RegexValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
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

    class Meta:
        verbose_name='Теги'

    def __str__(self):
        return self.name



class Ingredient(models.Model):
    name = models.CharField(
        blank=False,
        max_length=50,
        help_text='Укажите название ингредиента',
    )
    measurement_unit = models.CharField(
        blank=False,
        help_text='Введите единицу измерения',
        max_length=30,
    )

    class Meta:
        verbose_name='Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        help_text='Введите имя автора рецепта',
        verbose_name='Автор',
        related_name='recipes',
    )
    name = models.CharField(
        blank=False,
        help_text='Введите название рецепта',
        max_length=30,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        blank=False,
        upload_to='recipes/images/',
        verbose_name='Фото',
    )
    text = models.CharField(
        blank=False,
        help_text='Придумайте описание',
        max_length=100,
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        help_text='Выберите ингредиенты',
        verbose_name='Список ингредиентов',
        related_name='recipe',
        through='IngredientReciepe',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        help_text='Выберите теги',
        verbose_name='Список тегов',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        blank=False,
        help_text='Введите время приготовления(в минутах)',
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name='Рецепты'

    def __str__(self):
        return self.name


class IngredientReciepe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredient',
    )
    amount = models.PositiveIntegerField(
        help_text='Введите количество продукта',
        verbose_name='Количество',
    )


    class Meta:
        verbose_name = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient_for_recipe'
            )
        ]
    def __str__(self):
        return f'{self.ingredient}, {self.amount}'
    


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite',
    )

    class Meta:
        verbose_name = 'Избранные'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ('id',)
        verbose_name='Покупки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_recipe_in_shoppingcart'
            ),
        )
        
