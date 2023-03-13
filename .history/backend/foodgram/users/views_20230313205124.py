from rest_framework import serializers
from .models import User, Follow
from recipes.models import Recipe
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import UserGetSerializer
from recipes.serializers import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from .serializers import FollowSerializer

@action(detail=True, methods=['DELETE', 'POST'])
def follow(request, pk):
    if request.method == 'POST':
        author = get_object_or_404(User, pk=pk)
        user = get_object_or_404(User, username=request.user.username)
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
        try:
            subscribed = Follow.objects.get(user=user, author=author)
        except Exception:
            content = {'errors': 'Вы не подписаны на этого автора'}
            return Response(content, status=HTTP_400_BAD_REQUEST)
        subscribed.delete()
        return Response(status=HTTP_204_NO_CONTENT)

