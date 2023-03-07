from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path('auth/token/login', views.obtain_auth_token),
    #path('auth/token/logout')
]
