from rest_framework import serializers
from .models import User, Follow
from api.models import Recipe
from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets, status
from recipes.serializers import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from .serializers import UserGetSerializer, FollowSerializer
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer(many=True)

    @action(detail=True, methods=['DELETE', 'POST'])
    @permission_classes([permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if request.method == 'POST':
            author = get_object_or_404(User, pk=pk)
            user = request.user
            if user.id == author.id:
                content = {'errors': 'Невозможно подписаться на себя'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            try:
                Follow.objects.create(user=user, author=author)
            except Exception:
                content = {'errors': 'Вы уже подписаны на этого автора'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            follows = User.objects.all().filter(username=author)
            serializer = FollowSerializer(
                follows,
                context = {'request': request},
            )
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            author = get_object_or_404(User, pk=pk)
            user = get_object_or_404(User, username=request.username)
            try:
                subscribed = Follow.objects.get(user=user, author=author)
            except Follow.DoesNotExist:
                content = {'errors': 'Вы не подписаны на этого автора'}
                return Response(content, status=HTTP_400_BAD_REQUEST)
            subscribed.delete()
            return Response(status=HTTP_204_NO_CONTENT)


    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
