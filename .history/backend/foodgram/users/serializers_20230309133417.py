from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователя"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')

class UserGetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                 'first_name', 'last_name', 'is_subscribed')
        depth = 1

# class RegistrationSerializer(serializers.ModelSerializer):
#     """Серилайзер для регистрации"""
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     username = serializers.CharField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     class Meta:
#         model = User
#         fields = ('email', 'id',
#                   'username', 'first_name', 'last_name')