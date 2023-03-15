import base64

from api.models import Ingredient, IngredientReciepe, Recipe, Tag
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import UserGetSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class TagSerializers(serializers.ModelSerializer):

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
    name = serializers.CharField(source='ingredients.name', required=False)
    measurement_unit = serializers.CharField(source='ingredients.measurement_unit', required=False)
    amount = serializers.CharField(read_only=True)

    class Meta:
        model = IngredientReciepe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и создания рецептов"""

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientRecipeSerializer(source='recipes', many=True)
    author = UserGetSerializer(read_only=True)
    

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
    
    
    def create_ingredients(self, ingredients, recipes):
        for ingredient in ingredients:
            ingredient_obj = ingredient['id']
            amount = ingredient['amount']
            IngredientReciepe.objects.create(
                recipes=recipes, ingredient=ingredient_obj,
                amount=amount,
            )
            print(ingredient_obj, amount)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        print(validated_data.keys())
        ingredients_data = validated_data.pop('ingredients')
        recipes = Recipe.objects.create(
            author=author, **validated_data
        )
        self.create_ingredients(ingredients_data, recipes)
        recipes.tags.set(tags_data)
        return recipes

