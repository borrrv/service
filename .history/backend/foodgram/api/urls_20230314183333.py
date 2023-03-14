from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, RecipesViewSet, IngredientViewSet
from users.views import Follow

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', FollowViewSet)

urlpatterns = [
    path('api/users/<int:pk>/subscribe/', follow),
    path('api/', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
]
