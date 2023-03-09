from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, UserSerializer, UserGetSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    @action(
        detail=False,
        methods=['get'],
        serializer_class=UserGetSerializer,
    )
    
    """Список пользователей"""
    def get_list(self, request):
        users = User.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


