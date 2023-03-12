from .models import Recipe, Ingredient, Tag, IngredientReciepe
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile


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
            'name_tag',
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
            'amount',
            'unit',
        )


class IngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount',
        )

class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и создания рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True,
    )
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientGetSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
    

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_obj = ingredient['id']
            amount = ingredient['amount']
            IngredientReciepe.objects.create(
                recipe=recipe, ingredient=ingredient_obj,
                amount=amount,
            )

    # def create(self, validated_data):
    #     author = self.context.get('request').user
    #     tags_data = validated_data.pop('tags')
    #     ingredients_data = validated_data.pop('ingredients')
    #     image = validated_data.pop('image')
    #     recipes = Recipe.objects.create(
    #         image=image, **validated_data
    #     )
    #     self.create_ingredients(ingredients_data, recipes)
    #     recipes.tags.set(tags_data)
    #     return recipes
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.create(**ingredient_data)
            amount = ingredient_data['amount']
            unit = ingredient_data['unit']
            IngredientReciepe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount, unit=unit)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name_tag=tag_data['name_tag'], slug=tag_data['slug'], color=tag_data['color'])
            recipe.tags.add(tag)
        return recipe


