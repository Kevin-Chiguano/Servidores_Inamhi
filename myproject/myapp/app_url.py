from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import register, home
from django.conf import settings
from django.conf.urls.static import static

# Importa las vistas de tickets


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('admin', views.login_required, name='login'),
    path('model_list/', views.model_list, name='model_list'),
    path('create/', views.model_create, name='model_create'),
    path('<int:pk>/', views.model_detail, name='model_detail'),
    path('<int:pk>/update/', views.model_update, name='model_update'),
    path('<int:pk>/delete/', views.model_delete, name='model_delete'),
    path('<int:pk>/delete/confirm/', views.model_confirm_delete, name='model_confirm_delete'),
    path('<int:pk>/update/confirm/', views.model_confirm_actualizar, name='model_confirm_actualizar'),
    path('export/', views.export_to_excel, name='export_to_excel'),
    path('exportpdf/', views.export_to_pdf, name='export_to_pdf'),
    path('nodos/create/', views.nodos_create, name='nodos_create'),
    path('nodos/<int:pk>/', views.nodos_detail, name='nodos_detail'),
    path('nodos/<int:pk>/update/', views.nodos_update, name='nodos_update'),
    path('nodos/<int:pk>/delete/', views.nodos_delete, name='nodos_delete'),
    path('salir/', views.salir, name="salir")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
