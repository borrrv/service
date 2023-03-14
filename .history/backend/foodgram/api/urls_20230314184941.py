from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, RecipesViewSet, IngredientViewSet
from users.views import FollowGetViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users/subscriptions', FollowGetViewSet)

urlpatterns = [
    path('users/<int:pk>/subscribe/,'),
    path('api/', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
]
