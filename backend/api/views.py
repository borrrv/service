from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import (Favorites, Ingredient, IngredientReciepe, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow, User

from .filters import RecipesFilter
from .paginations import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (AddRecipesSerializer, FavoriteSerializer,
                          FollowSerializer, IngredientSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserNewSerializer)


class UsersNewViewSet(UserViewSet):
    """
    Вьюсет для добавления, удаления и просмотра подписок
    И для работы пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserNewSerializer
    pagination_class = CustomPagination

    @action(detail=True, methods=['DELETE', 'POST'],
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribed = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                content = {'errors': 'Невозможно подписаться на себя'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            if subscribed.exists():
                content = {'errors': 'Вы уже подписаны'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(author, context={'request': request})
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            if subscribed.exists():
                subscribed.delete()
                content = {'message': 'Вы успешно отписались'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'errors': 'Вы не подписаны на этого автора'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тега"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ('recipes__name',)
    permission_classes = (AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для получения и создания рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = AddRecipesSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ['POST, DELETE, PATCH']:
            self.permission_classes = [IsAuthorOrReadOnly]
        return super(RecipesViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        content = {'message': 'Рецепт успешно удален'}
        super().destroy(request, *args, **kwargs)
        return Response(content, status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite_and_shopping_cart(self, pk,
                                   serializer_class, model_class):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        object = model_class.objects.filter(user=user, recipe=recipe)
        if self.request.method == 'POST':
            if object.exists():
                return Response(status=HTTP_400_BAD_REQUEST)
            serializer = serializer_class(
                data={'user': user.id, 'recipe': pk},
                context={'request': self.request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if object.exists():
                object.delete()
                content = {'message': 'Успешно удалено'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'error': 'Ошибка'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk=None):
        return self.favorite_and_shopping_cart(pk, FavoriteSerializer,
                                               Favorites)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        return self.favorite_and_shopping_cart(pk, ShoppingCartSerializer,
                                               ShoppingCart)

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
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
