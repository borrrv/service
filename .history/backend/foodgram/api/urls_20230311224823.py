from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, RecipesViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
    
]
