from django.urls import path
from djoser.views import TokenCreateView
from rest_framework.authtoken import views
from users.views import registration

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view()),
    path('users/', registration, name='registration')
]
