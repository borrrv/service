from .models import User, Follow
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(UserCreateSerializer):
    """Сериалайзер для пользователя"""

    class Meta:
        model = User
        fields = (
                'email',
                'username',
                'first_name',
                'last_name',
                'password',
            )

class UserGetSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
                'email',
                'id',
                'username',
                'first_name',
                'last_name',
                'is_subscribed',
            )
        read_only_fields = ('role',)


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = 