from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipesViewSet, TagViewSet,
                       UsersViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipesViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
