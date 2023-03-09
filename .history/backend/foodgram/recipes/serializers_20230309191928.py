from .models import Recipe, Ingridient, Tag, IngridientReciepe
from rest_framework import serializers

class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name_tag',
                  'color',
                  'slug',
                )