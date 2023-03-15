# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('', include('api.urls')),
#     path('admin/', admin.site.urls),
#     path('api/users/', include('djoser.urls')),
#     path('api/auth/', include('djoser.urls.authtoken')),
# ]
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
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
