from rest_framework import serializers
from .models import User, Follow
from recipes.models import Recipe
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .serializers import UserGetSerializer
from recipes.serializers import Recipe
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


@action(detail=True, methods=['POST'])
def follow(request, pk):
    author = get_object_or_404(User, pk=pk)
    user = get_object_or_404(User, username=request.user.username)
        

