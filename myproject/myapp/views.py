from django.shortcuts import render, redirect, get_object_or_404
from .models import Servidores
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.utils import timezone
from django.contrib import messages
from .models import Nodos,ApisYsubdominios
from .forms import NodosForm
from .forms import FormularioForm, Formulario, SubdominioForm, Subdominios
from .forms import MyModelForm, CustomUserCreationForm,ApisYsubdominiosForm
import pytz

def home(request):
    return render(request, 'registration/login.html')

def register(request):
    data = {'form': CustomUserCreationForm()}
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, '¡Usuario registrado correctamente!')
                return redirect('register')
    return render(request, 'registration/register.html', data)

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_detail(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    context = {
        'user': request.user.get_full_name(),
        'model': model
    }
    return render(request, 'model_detail.html', {'model': model})

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_list(request):
    models = Servidores.objects.all()
    nodos = Nodos.objects.all()
    apis = ApisYsubdominios.objects.all()
    formulario = Formulario.objects.all()
    subdominios = Subdominios.objects.all()

    return render(request, 'model_list.html', {
        'models': models,
        'nodos': nodos,
        'apis': apis,
        'formulario': formulario,
        'subdominios': subdominios


    })

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            for field_name, field_value in instance.__dict__.items():
                if not field_value and field_name != 'id':
                    setattr(instance, field_name, 'VACÍO')
            instance.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})


@login_required
def model_update(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            model = form.save(commit=False)
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
            model.save()
            return redirect('model_list')  # Redirigir a la lista de modelos después de la actualización
    else:
        form = MyModelForm(instance=model)

    return render(request, 'actualizar.html', {'form': form, 'model': model})


@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_confirm_actualizar(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('model_list')
    else:
        form = MyModelForm(instance=model)
    return render(request, 'model_confirm_actualizar.html', {'form': form, 'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_delete(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    if request.method == 'POST':
        model.estado_registro = False
        model.delete()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_confirm_delete(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
def salir(request):
    logout(request)
    return redirect('/')

# Exportación a Excel
def export_to_excel_servidores(request):
    queryset = Servidores.objects.all()

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['DireccionIp', 'Usuario', 'Contrasena', 'Servicio', 'Puerto', 'RutaImportante', 
                    'UbicacionFisica', 'NumeroSerie']
    ws.append(column_names)

    # Escribir datos de los objetos en el libro
    for obj in queryset:
        ws.append([obj.DireccionIp, obj.Usuario, obj.Contrasena, obj.Servicio, obj.Puerto, obj.RutaImportante, obj.UbicacionFisica, 
                   obj.NumeroSerie])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Servidores_Report.xlsx'
    wb.save(response)
    return response
#Nodo ------------------------------------------------------------------------
@login_required
@permission_required('myapp.view_nodos', raise_exception=True)
def nodos_list(request):
    nodos = Nodos.objects.all()
    return render(request, 'model_list.html', {'nodos': nodos})

@login_required
@permission_required('myapp.add_nodos', raise_exception=True)
def nodos_create(request):
    if request.method == 'POST':
        form = NodosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Nodo creado correctamente!')
            return redirect('model_list')
    else:
        form = NodosForm()
    return render(request, 'nodos/nodos_form.html', {'form': form})

@login_required
@permission_required('myapp.change_nodos', raise_exception=True)
def nodos_update(request, pk):
    nodo = get_object_or_404(Nodos, pk=pk)
    if request.method == 'POST':
        form = NodosForm(request.POST, instance=nodo)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Nodo actualizado correctamente!')
            return redirect('model_list')
    else:
        form = NodosForm(instance=nodo)
    return render(request, 'nodos/nodos_form.html', {'form': form, 'nodo': nodo})

@login_required
@permission_required('myapp.delete_nodos', raise_exception=True)
def nodos_delete(request, pk):
    nodo = get_object_or_404(Nodos, pk=pk)
    if request.method == 'POST':
        nodo.delete()
        messages.success(request, '¡Nodo eliminado correctamente!')
        return redirect('model_list')
    return render(request, 'nodos/nodos_confirm_delete.html', {'nodo': nodo})

@login_required
@permission_required('myapp.view_nodos', raise_exception=True)
def nodos_detail(request, pk):
    nodo = get_object_or_404(Nodos, pk=pk)
    return render(request, 'nodos/nodos_detail.html', {'nodo': nodo})


# Exportación a Excel NODOS
def export_nodos_to_excel(request):
    queryset = Nodos.objects.all()

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['Host', 'Usuario', 'Ram', 'Disco', 'SistemaOperativo', 'Descripcion', 'Contrasena']
    ws.append(column_names)

    # Escribir datos de los objetos en el libro
    for obj in queryset:
        ws.append([obj.Host, obj.Usuario, obj.Ram, obj.Disco, obj.SistemaOperativo, obj.Descripcion, obj.Contrasena])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Nodos_Report.xlsx'
    wb.save(response)
    return response

# APIS -----------------------------------------------------------------------


@login_required
@permission_required('myapp.view_apisysubdominios', raise_exception=True)
def apis_view(request):
    apis = ApisYsubdominios.objects.all()
    return render(request, 'model_list.html', {'apis': apis})

@login_required
@permission_required('myapp.add_apisysubdominios', raise_exception=True)
def apis_create(request):
    if request.method == 'POST':
        form = ApisYsubdominiosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡API creada correctamente!')
            return redirect('model_list')
    else:
        form = ApisYsubdominiosForm()
    return render(request, 'crear_apis.html', {'form': form})

@login_required
@permission_required('myapp.change_apisysubdominios', raise_exception=True)
def apis_update(request, pk):
    api = get_object_or_404(ApisYsubdominios, pk=pk)
    if request.method == 'POST':
        form = ApisYsubdominiosForm(request.POST, instance=api)
        if form.is_valid():
            form.save()
            messages.success(request, '¡API actualizada correctamente!')
            return redirect('model_list')
    else:
        form = ApisYsubdominiosForm(instance=api)
    return render(request, 'apis_update.html', {'form': form, 'api': api})

@login_required
@permission_required('myapp.delete_apisysubdominios', raise_exception=True)
def apis_delete(request, pk):
    api = get_object_or_404(ApisYsubdominios, pk=pk)
    if request.method == 'POST':
        api.delete()
        messages.success(request, '¡API eliminada correctamente!')
        return redirect('model_list')
    return render(request, 'apis_confirm_delete.html', {'api': api})

@login_required
@permission_required('myapp.view_apisysubdominios', raise_exception=True)
def apis_detail(request, pk):
    api = get_object_or_404(ApisYsubdominios, pk=pk)
    return render(request, 'apis_detail.html', {'api': api})


import openpyxl
from django.http import HttpResponse
from .models import ApisYsubdominios

def export_apisysubdominios_to_excel(request):
    # Crear un libro de trabajo y una hoja de trabajo
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Apis y Subdominios'

    # Agregar encabezados de columna
    headers = ['Nombre Servicio HTTPS', 'Descripción', 'IP', 'Puerto']
    worksheet.append(headers)

    # Obtener datos del modelo
    apis = ApisYsubdominios.objects.all()

    # Agregar datos a la hoja de trabajo
    for api in apis:
        row = [
            api.NombreServicioHttps,
            api.Descripcion,
            api.Ip,
            api.puerto
        ]
        worksheet.append(row)

    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Apis_Report.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response


#Formularios ------------------------------------------------------------------------
@login_required
@permission_required('myapp.view_formulario', raise_exception=True)
def formulario_list(request):
    formulario = formulario.objects.all()
    return render(request, 'model_list.html', {'formulario': formulario})

@login_required
@permission_required('myapp.add_formulario', raise_exception=True)
def formulario_create(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Formulario creado correctamente!')
            return redirect('model_list')
    else:
        form = FormularioForm()
    return render(request, 'formulario/formulario_form.html', {'form': form})

@login_required
@permission_required('myapp.change_formulario', raise_exception=True)
def formulario_update(request, pk):
    formulario = get_object_or_404(Formulario, pk=pk)
    if request.method == 'POST':
        form = FormularioForm(request.POST, instance=formulario)
        if form.is_valid():
            form.save()
            messages.success(request, '!Formulario actualizado correctamente!')
            return redirect('model_list')
    else:
        form = FormularioForm(instance=formulario)
    return render(request, 'formulario/formulario_form.html', {'form': form, 'formulario': formulario})

@login_required
@permission_required('myapp.delete_formulario', raise_exception=True)
def formulario_delete(request, pk):
    formulario = get_object_or_404(Formulario, pk=pk)
    if request.method == 'POST':
        formulario.delete()
        messages.success(request, '¡Formulario eliminado correctamente!')
        return redirect('model_list')
    return render(request, 'formulario/formulario_confirm_delete.html', {'formulario': formulario})


@login_required
@permission_required('myapp.view_formulario', raise_exception=True)
def formulario_detail(request, pk):
    formulario = get_object_or_404(Formulario, pk=pk)
    return render(request, 'formulario/formulario_detail.html', {'formulario': formulario})


# Exportación a Excel
def export_to_excel(request):
    queryset = Formulario.objects.all()

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['NombreServidor', 'Ubicacion', 'Marca', 'Modelo', 'NumeroSerie', 'SistemaOperativo', 
                    'PuertoRelevante', 'Entorno','Estado','DireccionIpLocal','DireccionIpPublica','Usuario','Clave','DescripcionProcesos']
    ws.append(column_names)

    # Escribir datos de los objetos en el libro
    for obj in queryset:
        ws.append([obj.NombreServidor, obj.Ubicacion, obj.Marca, obj.Modelo, obj.NumeroSerie, obj.SistemaOperativo, 
                   obj.PuertoRelevante, obj.Entorno, obj.Estado, obj.DireccionIpLocal, obj.DireccionIpPublica, obj.Usuario, obj.Clave, obj.DescripcionProcesos])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Forumulario_Report.xlsx'
    
    wb.save(response)
    return response

#Subdominio ----------------------------------------------------------------------------
# Lista de Subdominios
@login_required
@permission_required('myapp.view_subdominios', raise_exception=True)
def subdominios_list(request):
    subdominios = Subdominios.objects.all()
    return render(request, 'model_list.html', {'subdominios': subdominios})

# Crear Subdominio
@login_required
@permission_required('myapp.add_subdominios', raise_exception=True)
def subdominios_create(request):
    if request.method == 'POST':
        form = SubdominioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Subdominio creado correctamente!')
            return redirect('model_list')  # Redirige a la página con la lista de subdominios
    else:
        form = SubdominioForm()
    return render(request, 'subdominios/subdominios_form.html', {'form': form})

# Actualizar Subdominio
@login_required
@permission_required('myapp.change_subdominios', raise_exception=True)
def subdominios_update(request, pk):
    subdominio = get_object_or_404(Subdominios, pk=pk)
    if request.method == 'POST':
        form = SubdominioForm(request.POST, instance=subdominio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Subdominio actualizado correctamente!')
            return redirect('model_list')  # Redirige a la página con la lista de subdominios
    else:
        form = SubdominioForm(instance=subdominio)
    return render(request, 'subdominios/subdominios_form.html', {'form': form, 'subdominio': subdominio})

# Eliminar Subdominio
@login_required
@permission_required('myapp.delete_subdominios', raise_exception=True)
def subdominios_delete(request, pk):
    subdominio = get_object_or_404(Subdominios, pk=pk)
    if request.method == 'POST':
        subdominio.delete()
        messages.success(request, '¡Subdominio eliminado correctamente!')
        return redirect('model_list')  # Redirige a la página con la lista de subdominios
    return render(request, 'subdominios/subdominios_confirm_delete.html', {'subdominio': subdominio})

# Detalle del Subdominio
@login_required
@permission_required('myapp.view_subdominios', raise_exception=True)
def subdominios_detail(request, pk):
    subdominio = get_object_or_404(Subdominios, pk=pk)
    return render(request, 'subdominios/subdominios_detail.html', {'subdominio': subdominio})

# Exportación a Excel
def export_to_excel_subdominios(request):
    queryset = Subdominios.objects.all()

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['Id', 'Nombre', 'IpPublica', 'IpInterna', 'Host']
    ws.append(column_names)

    # Escribir datos de los objetos en el libro
    for obj in queryset:
        ws.append([obj.Id, obj.Nombre, obj.IpPublica, obj.IpInterna, obj.Host])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Subdominio_Report.xlsx'
    wb.save(response)
    return response
