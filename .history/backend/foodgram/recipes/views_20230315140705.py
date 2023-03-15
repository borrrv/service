from django.shortcuts import render
from api.models import Tag, Recipe, Ingredient, IngredientReciepe
from rest_framework.decorators import action
from .serializers import TagSerializers, IngredientSerializer, RecipesSerializer, IngredientRecipeSerializer
from rest_framework.response import Response
from rest_framework import viewsets


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для получения и создания рецептов"""

    queryset = IngredientReciepe.objects.all()
    serializer_class = IngredientRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None