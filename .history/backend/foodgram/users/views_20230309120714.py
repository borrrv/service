from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """Регистрация пользователя"""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_users(request):
    №serializer.is_valid(raise_exception=True)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=HTTP_200_OK)