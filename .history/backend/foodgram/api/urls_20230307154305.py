from django.urls import path
from djoser.views import TokenCreateView
from rest_framework.authtoken import views
from users.views import registration

urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('users/', registration, name='registration')
]
