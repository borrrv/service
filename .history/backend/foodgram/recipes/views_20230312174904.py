from django.shortcuts import render
from .models import Tag, Recipe, Ingredient
from rest_framework.decorators import action
from .serializers import TagSerializers, IngridientSerializer, RecipesSerializer
from rest_framework.response import Response
from rest_framework import viewsets


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для получения и создания рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None