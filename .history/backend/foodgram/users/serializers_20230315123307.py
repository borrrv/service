from .models import User, Follow
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from api.models import Recipe

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
    """Сериалайзер для отображения информации о пользователе"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

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

    def get_is_subscribed(self, object):
        """Подписан ли пользователь на автора"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=object.id).exists()

class ShortFollowSerializer(serializers.ModelSerializer):
    """Сериалайзер для короткого рецепта в подписках"""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(UserGetSerializer):
    """Сериалайзер для добавления, удаления и просмотра подписок"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortFollowSerializer(recipes, many=True).data
    
    # def get_recipes_count(self, obj):
    #     return obj.recipes.count()