from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('registrarticket/', views.registrarticket), #recive el id no sirve para editar los datos y me envia a otra plantilla
    path('editarticket/<id>/', views.editarticket),
    path('eliminarticket/<id>', views.eliminarticket),
    # Otros patrones de URL para las vistas de tickets
]
