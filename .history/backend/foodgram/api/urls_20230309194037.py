from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from recipes.views import get_tag

router = DefaultRouter()


router.register(r'tags', get_tag)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
    
]
