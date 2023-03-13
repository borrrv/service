from rest_framework import serializers
from .models import User, Follow
from recipes.models import Recipe
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import UserGetSerializer
from recipes.serializers import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

@action(detail=True, methods=['POST'])
def follow(request, pk):
    author = get_object_or_404(User, pk=pk)
    user = get_object_or_404(User, username=request.user.username)
    if user.id == author.id:
        content = {'errors': 'Невозможно подписаться на себя'}
        return Response(content, status=HTTP_400_BAD_REQUEST)
        

