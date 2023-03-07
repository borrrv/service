from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        GUEST: 'guest',
        USER: 'user',
        ADMIN: 'admin'
    ]