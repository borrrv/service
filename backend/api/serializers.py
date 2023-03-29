from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from recipes.models import (Favorites, Ingredient, IngredientReciepe, Recipe,
                            ShoppingCart, Tag)
from users.models import User


class UserNewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения информации о пользователе"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, object):
        """Подписан ли пользователь на автора"""
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=object).exists()


class ShortFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для короткого рецепта в подписках"""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(UserNewSerializer):
    """Сериалайзер для добавления, удаления и просмотра подписок"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, object):
        request = self.context.get('request')
        recipes = object.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                raise ValidationError('Ожидается int')
        return ShortFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """Сериалазер для тега"""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода ингридиентов"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения ингридиентов в рецептах"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )
    name = serializers.CharField(
        source='ingredient.name',
        required=False,
        read_only=True
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.CharField()

    class Meta:
        model = IngredientReciepe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientAddRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления ингредиентов при создании рецептов"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',)

    class Meta:
        model = IngredientReciepe
        fields = ('id', 'amount',)


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения рецептов"""

    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
    )
    author = UserNewSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return object.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return object.shopping_cart.filter(user=user).exists()


class AddRecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецептов"""
    author = UserNewSerializer(read_only=True)
    image = Base64ImageField(required=False)
    ingredients = IngredientAddRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('name',),
                message=('Рецепт с таким названием уже есть'),
            )
        ]

    def validate_ingredients(self, value):
        ingredient_list = [ingredient for ingredient, amount in value]
        unique_ingredients = set(ingredient_list)
        if len(unique_ingredients) != len(ingredient_list):
            raise ValidationError(
                'Ингредиенты не должны повторяться'
            )
        return value

    def create_ingredients(self, instance, ingredients):
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient_obj = ingredient['ingredient']
            IngredientReciepe.objects.create(
                recipe=instance,
                ingredient=ingredient_obj,
                amount=amount,
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=author,
            name=validated_data['name'],
            image=validated_data.get('image'),
            text=validated_data.get('text'),
            cooking_time=validated_data.get('cooking_time')
        )
        recipe.tags.set(tags_data)
        self.create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        tags = instance.tags.clear()
        IngredientReciepe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipesSerializer(instance, context=context).data


class FavoriteInfoSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для вывода информации о рецепте
    в избранном и списках покупок
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления в избранное"""

    class Meta:
        model = Favorites
        fields = (
            'user',
            'recipe',
        )

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return FavoriteInfoSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для добавления рецептов в список покупок"""

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return FavoriteInfoSerializer(instance.recipe, context=context).data
