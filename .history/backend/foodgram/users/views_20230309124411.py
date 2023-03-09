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

# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny])
# def registration(request):
#     """Регистрация пользователя"""
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=HTTP_200_OK)
#     users = User.objects.all()
#     serializer = UserGetSerializer(users, many=True)
#     return Response(serializer.data, status=HTTP_200_OK)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # @action(
    #     methods=['post', 'get']
    # )
    # def 
