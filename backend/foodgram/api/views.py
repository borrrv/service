from api.models import (Favorites, Ingredient, IngredientReciepe, Recipe,
                        ShoppingCart, Tag)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from django.http import FileResponse, HttpResponse

from .serializers import (AddRecipesSerializer, FavoriteSerializer,
                          IngredientRecipeSerializer, IngredientSerializer,
                          RecipesSerializer, TagSerializer, ShoppingCartSerializer)
from users.models import User

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для получения и создания рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = AddRecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        content = {'message': 'Рецепт успешно удален'}
        super().destroy(request, *args, **kwargs)
        return Response(content, status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorites.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if favorite.exists():
                content = {'error': 'Рецепт уже есть в избранном'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            content = {'messaage': 'Рецепт успешно добавлен в избранное'}
            return Response(content, status=HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                content = {'message': 'Рецепт успешно удален из избранного'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'errors': 'Этот рецепт не в избранном'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'GET', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe.id)
        if request.method == 'POST':
            if shopping_cart.exists():
                content = {'errors': 'Данный рецепт уже есть в списке покупок'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            serializer = ShoppingCartSerializer(data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            content = {'message': 'Рецепт успешно добавлен в список покупок'}
            return Response(content, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                content = {'message': 'Рецепт успешно удален из списка покупок'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'errors': 'Этого рецепта нет в списке покупок'}
            return Response(content, status=HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
