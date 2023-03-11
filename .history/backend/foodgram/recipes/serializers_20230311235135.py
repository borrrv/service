from .models import Recipe, Ingridient, Tag, IngridientReciepe
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

class RecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'ingridients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = (
            'id',
            'name_ingridient',
            'unit',
        )
        extra_kwargs = {'name_ingridient': {'required': False},
                        'unit': {'required': False}}
