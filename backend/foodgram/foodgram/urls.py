from api.views import IngredientViewSet, RecipesViewSet, TagViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
]
