from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверка метод запроса безопасен или
           пользователь имеет подходящую роль."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_user
            or request.user.is_admin
            or request.user == obj.author
        )

    def has_permission(self, request, view):
        """Проверка метод запроса безопасен или
           пользователь авторизован."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated)
