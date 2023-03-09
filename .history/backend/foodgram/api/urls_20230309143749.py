from django.urls import path, include
from rest_framework.authtoken import views
from users.views import UsersViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin

router = DefaultRouter()

router.register(r'users', UsersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, namespace='admin'),
    path('auth/token/login/', views.obtain_auth_token),
    path('', include(router.urls)),
]
