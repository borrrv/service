import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import UserGetSerializer

from .models import (Favorites, Ingredient, IngredientReciepe, Recipe,
                     ShoppingCart, Tag)


class Base64ImageField(serializers.ImageField):
    """Кодирование изображения"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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
    )
    name = serializers.CharField(source='ingredient.name', required=False, read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
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
    ingredients = IngredientRecipeSerializer(source='recipe_ingredient', many=True)
    author = UserGetSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
    
    def get_is_favorite(self, object):
        user = self.context.get('request').user
        return object.favorite.filter(user=user).exists()

    def get_is_shopping_cart(self, object):
        user = self.context.get('request').user
        return object.shopping_cart.filter(user=user).exists()
    

class AddRecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания рецептов"""
    author = UserGetSerializer(read_only=True)
    image = Base64ImageField()
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

    def create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient_obj = ingredient['ingredient']
            IngredientReciepe.objects.create(
                recipe=recipe, ingredient=ingredient_obj,
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
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        IngredientReciepe.objects.filter(recipe=instance).delete()
        instance.tags.set(tags_data)
        self.create_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipesSerializer(instance, context=context).data
    

class FavoriteInfoSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода информации о рецепте в избранном и списках покупок"""
    
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
