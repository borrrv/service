from django.urls import path
from rest_framework.authtoken import views
from users.views import registration, UsersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UsersViewSet)

urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('users/', registration, name='registration'),
    path('users/<int:pk>', UsersViewSet, name='get_list'),
]
