from .models import Recipe, Ingredient, Tag
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

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit',
        )


class RecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и создания рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True,
    )
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


