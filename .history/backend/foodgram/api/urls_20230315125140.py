from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, RecipesViewSet, IngredientViewSet
from users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
]