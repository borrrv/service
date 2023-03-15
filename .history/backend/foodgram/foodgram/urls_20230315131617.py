from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
