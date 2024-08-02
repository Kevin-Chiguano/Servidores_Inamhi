from django.contrib import admin
from django.urls import path, include
from tickets import views
from myapp.views import register, recover

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.app_url')),  # Se incluye el archivo de URLs de myapp
    path('tickets/', include('tickets.urls')), 
    path('registrarticket/', views.registrarticket, name='registrarticket'), # Se incluye el archivo de URLs de tickets
    path('eliminarticket/', views.eliminarticket, name='eliminarticket'),
    path('editarticket/<int:id>/', views.editarticket, name='editarticket'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('recover/', recover, name='recover'),
   
]
