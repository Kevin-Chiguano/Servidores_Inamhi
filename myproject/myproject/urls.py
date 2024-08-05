from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.app_url')),  # Se incluye el archivo de URLs de myapp
    path('accounts/', include('django.contrib.auth.urls')),
   
]
