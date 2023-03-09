from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from djoser.serializers import UserCreateSerializer, UserSerializer

class UserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для пользователя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('email', 'username',
                  'first_name', 'last_name', 'password',)

class UserGetSerializer(UserSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    result = serializers.CharField()
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                 'first_name', 'last_name', 'is_subscribed')
        #depth = 1