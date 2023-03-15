
from .models import User, Follow
from rest_framework.decorators import action, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from .serializers import UserGetSerializer, FollowSerializer
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer

    @action(detail=True, methods=['DELETE', 'POST'])
    @permission_classes([permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)
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
                content = {'message':'Вы успешно отписались'}
                return Response(content, status=HTTP_204_NO_CONTENT)
            content = {'errors': 'Вы не подписаны на этого автора'}
            return Response(content, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        follows = User.objects.filter(following__user=user)
        page = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
