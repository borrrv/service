from .models import User
from djoser.serializers import UserSerializer, UserCreateSerializer

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
