from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r'tags', )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
    
]
