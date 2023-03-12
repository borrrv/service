from django.shortcuts import render
from .models import Tag, Recipe, Ingridient
from rest_framework.decorators import action
from .serializers import TagSerializers, RecipesSerializer, IngridientSerializer
from rest_framework.response import Response
from rest_framework import viewsets


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngridientViewSet(viewsets.ModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None