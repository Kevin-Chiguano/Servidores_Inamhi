from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import register, home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('home/', home, name='home'),  # Cambiado de '' a 'home/' para evitar conflicto
    path('register/', register, name='register'),
    path('admin/', views.login_required, name='login'),  # Asegúrate de que la vista `login_required` esté bien definida
    path('model_list/', views.model_list, name='model_list'),
    path('create/', views.model_create, name='model_create'),
    path('model/<int:pk>/', views.model_detail, name='model_detail'),  # Prefijo 'model/' agregado
    path('model/<int:pk>/update/', views.model_update, name='model_update'),
    path('model/<int:pk>/delete/', views.model_delete, name='model_delete'),
    path('model/<int:pk>/delete/confirm/', views.model_confirm_delete, name='model_confirm_delete'),
    path('model/<int:pk>/update/confirm/', views.model_confirm_actualizar, name='model_confirm_actualizar'),
    path('export/', views.export_to_excel, name='export_to_excel'),
     path('export_apis/', views.export_apisysubdominios_to_excel, name='export_apisysubdominios'),  # Exportar datos de ApisYsubdominios a Excel
    path('nodos/export/', views.export_nodos_to_excel, name='export_nodos_to_excel'),  # Nueva ruta para exportar nodos a Excel
    path('exportpdf/', views.export_to_pdf, name='export_to_pdf'),
    path('nodos/create/', views.nodos_create, name='nodos_create'),
    path('nodos/<int:pk>/', views.nodos_detail, name='nodos_detail'),
    path('nodos/<int:pk>/update/', views.nodos_update, name='nodos_update'),
    path('nodos/<int:pk>/delete/', views.nodos_delete, name='nodos_delete'),
    path('apis/', views.apis_view, name='apis'),
    path('apis/create/', views.apis_create, name='crear_apis'),
    path('apis/<int:pk>/', views.apis_detail, name='apis_detail'),  # Prefijo 'apis/' agregado
    path('apis/<int:pk>/update/', views.apis_update, name='apis_update'),
    path('apis/<int:pk>/delete/', views.apis_delete, name='apis_delete'),
    path('formulario/create/', views.formulario_create, name='formulario_create'),
    path('formulario/<int:pk>/delete/', views.formulario_delete, name='formulario_delete'),
    path('formulario/<int:pk>/', views.formulario_detail, name='formulario_detail'),
    path('formulario/<int:pk>/update/', views.formulario_update, name='formulario_update'),
    path('formulario/<int:pk>/delete/', views.formulario_delete, name='formulario_delete'), 
    path('salir/', views.salir, name="salir")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
