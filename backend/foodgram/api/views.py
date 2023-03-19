from api.models import (Favorites, Ingredient, IngredientReciepe, Recipe,
                        ShoppingCart, Tag)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .permissions import IsAuthorOrReadOnly
from .serializers import (AddRecipesSerializer, FavoriteSerializer,
                          IngredientSerializer, ShoppingCartSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тега"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['recipes__name']
    permission_classes = (AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для получения и создания рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = AddRecipesSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['author',
                     'tags',
                     'favorite__recipe',
                     'shopping_cart__recipe']

    def get_permissions(self):
        if self.request.method in ['POST, DELETE, PATCH']:
            self.permission_classes = [IsAuthenticated]
        return super(RecipesViewSet, self).get_permissions()

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
                return Response(content,
                                status=HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

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
        shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe.id
        )
        if request.method == 'POST':
            if shopping_cart.exists():
                content = {'errors': 'Данный рецепт уже есть в списке покупок'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            serializer = ShoppingCartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            content = {'message': 'Рецепт успешно добавлен в список покупок'}
            return Response(content, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                content = {'message':
                           'Рецепт успешно удален из списка покупок'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'errors': 'Этого рецепта нет в списке покупок'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipes = IngredientReciepe.objects.filter(
            recipe__shopping_cart__user=user).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        shop = {}
        result = ''
        for ingredient, measurement_unit, amount in recipes:
            if ingredient not in shop:
                shop[ingredient] = {'measurement_unit': measurement_unit,
                                    'amount': amount}
            else:
                shop[ingredient]['amount'] += amount
        for ingr, res in shop.items():
            result += (f"{ingr.capitalize()}"
                       f"({res['measurement_unit']}) - {res['amount']}\n")
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = (
            "attachment; filename='shoppinng_list.txt'"
        )
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filtset_fields = ['name']
