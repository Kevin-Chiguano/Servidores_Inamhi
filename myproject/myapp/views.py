# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyModel, CambioCustodio
from .forms import MyModelForm, CambioCustodioForm, CustomUserCreationForm
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
from django.contrib.auth.models import Permission
from django.db import migrations
from reportlab.lib.units import inch
import pytz


def home(request):
    return render(request, 'registration/login.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
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


#Permisos required
@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_detail(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_detail.html', {'model': model})

@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_list(request):
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_create(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            for field_name, field_value in instance._dict_.items():
                if not field_value and field_name != 'id':
                    setattr(instance, field_name, 'VACÍO')
            instance.save()
            return redirect('model_list')
    else:
        form = MyModelForm()
    return render(request, 'model_form.html', {'form': form})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        cambio_form = CambioCustodioForm(request.POST)
        if form.is_valid() and cambio_form.is_valid():
            model = form.save(commit=False)
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
                model.save()

            cambio = model.cambiocustodio_set.first()
            if not cambio:
                cambio = CambioCustodio(modelo_relacionado=model)
            cambio.nuevo_custodio = cambio_form.cleaned_data['nuevo_custodio']
            cambio.cedula_nuevo_custodio = cambio_form.cleaned_data['cedula_nuevo_custodio']
            cambio.fecha_cambio = timezone.now()
            cambio.save()

            return redirect('model_list')
    else:
        form = MyModelForm(instance=model)
        cambio_form = CambioCustodioForm()

    return render(request, 'actualizar.html', {'form': form, 'cambio_custodio_form': cambio_form, 'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_confirm_actualizar(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form_data = request.session.get('form_data')
        if form_data:
            form = MyModelForm(form_data, instance=model)
            if form.is_valid():
                form.save()
                return redirect('model_list')
                
    else:
        form = MyModelForm(instance=model)
    return render(request, 'model_confirm_actualizar.html', {'form': form, 'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
@permission_required('myapp.can_view_mymodel', raise_exception=True)
def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        model.estado_registro = False
        model.save()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

# @login_required llama al login antes de que entre a el siguiente metodo
@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')

@login_required
def salir(request):
    logout(request)
    return redirect('/')
@login_required
def model_detail(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_detail.html', {'model': model})
@login_required
def model_list(request):
    models = MyModel.objects.all()
    return render(request, 'model_list.html', {'models': models})
@login_required
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
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        cambio_form = CambioCustodioForm(request.POST)
        if form.is_valid() and cambio_form.is_valid():
            model = form.save(commit=False)
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
                model.save()

            # Verificar si ya existe un objeto CambioCustodio para este modelo
            cambio = model.cambiocustodio_set.first()
            if not cambio:
                cambio = CambioCustodio(modelo_relacionado=model)
            cambio.nuevo_custodio = cambio_form.cleaned_data['nuevo_custodio']
            cambio.cedula_nuevo_custodio = cambio_form.cleaned_data['cedula_nuevo_custodio']
            cambio.fecha_cambio = timezone.now()  # Asigna la fecha actual
            cambio.save()

            return redirect('model_list')  # Redirigir a la lista de modelos después de la actualización
    else:
        form = MyModelForm(instance=model)
        cambio_form = CambioCustodioForm()

    return render(request, 'actualizar.html', {'form': form, 'cambio_custodio_form': cambio_form, 'model': model})


@login_required
def model_confirm_actualizar(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        # Guardar los cambios en la confirmación
        form_data = request.session.get('form_data')
        if form_data:
            form = MyModelForm(form_data, instance=model)
            if form.is_valid():
                form.save()
                return redirect('model_list')
                
    else:
        form = MyModelForm(instance=model)
    return render(request, 'model_confirm_actualizar.html', {'form': form, 'model': model})



@login_required
def model_confirm_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
def model_delete(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        # Cambiar el estado_registro a False y guardar el objeto
        model.estado_registro = False
        model.save()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

#Exportacion de EXCEL
def export_to_excel(request):
   
    queryset1 = MyModel.objects.filter(estado_registro=True)
    queryset2 = CambioCustodio.objects.filter(modelo_relacionado__in=queryset1)

    # Crear un libro de trabajo y una hoja de trabajo
    wb = Workbook()
    ws = wb.active

    # Escribir encabezados de columna
    column_names = ['codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo',
                    'nombre_bien', 'serie', 'modelo', 'marca', 'color', 'material', 'estado',
                    'ubicacion', 'cedula', 'custodio_actual', 'observacion', 'nuevo_custodio', 'cedula_nuevo_custodio', 'fecha_cambio']
    ws.append(column_names)

    # Crear un diccionario para almacenar los datos de CambioCustodio
    custodia_dict = {item.modelo_relacionado_id: item for item in queryset2}

    # Escribir datos de MyModel y agregar datos de CambioCustodio si están disponibles
    for item in queryset1:
        row = [getattr(item, col) for col in column_names[:15]]  # Datos de MyModel
        cambio = custodia_dict.get(item.id, None)
        if cambio:
            row.extend([cambio.nuevo_custodio, cambio.cedula_nuevo_custodio, cambio.fecha_cambio.strftime('%d-%m-%Y')])
        else:
            row.extend(['N/A', 'N/A', 'N/A'])
        ws.append(row)

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)
    return response

def export_to_pdf(request):
    
    queryset1 = MyModel.objects.filter(estado_registro=True)
    queryset2 = CambioCustodio.objects.filter(modelo_relacionado__in=queryset1)

    # Crear un archivo PDF
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))

    # Configurar estilos para el PDF
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TableStyle', fontSize=8, leading=10))
    font_size = 8  # Reducir el tamaño de la fuente para ajustarse mejor a las celdas

    # Añadir título y fecha de generación
    title = "Reporte de Bienes"
    timezone_bogota = pytz.timezone('America/Bogota')
    fecha_generacion = f"Fecha de generación: {timezone.localtime(timezone.now(), timezone_bogota).strftime('%d-%m-%Y %H:%M:%S')}"

    title_paragraph = Paragraph(title, styles['Title'])
    date_paragraph = Paragraph(fecha_generacion, styles['Normal'])

    # Crear datos para la tabla en el PDF
    data = []
    column_names = ['codigo_tic','codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo',
                    'nombre_bien', 'serie', 'cedula', 'custodio_actual',
                    'nuevo_custodio', 'cedula_nuevo_custodio']
    data.append(column_names)

    # Obtener los valores de los campos para cada objeto en queryset1
    for item in queryset1:
        row = []
        for col in column_names[:9]:  # Solo hasta 'archivo'
            value = getattr(item, col, None)
            if value is None:
                if hasattr(item, col):
                    related_obj = getattr(item, col)
                    value = str(related_obj)
                else:
                    value = 'N/A'
            elif isinstance(value, (str, int)):
                value = str(value)
            else:
                value = 'N/A'
            row.append(value)

        # Añadir valores por defecto para las columnas de CambioCustodio
        row.extend(['N/A', 'N/A', 'N/A'])
        data.append(row)

    # Actualizar las filas con datos de CambioCustodio
    for item in queryset2:
        for row in data:
            if row[0] == item.modelo_relacionado.codigo_bien:
                row[-3] = item.nuevo_custodio
                row[-2] = item.cedula_nuevo_custodio
                row[-1] = item.fecha_cambio.strftime('%d-%m-%Y')
                break


    # Calcular el ancho de la tabla en función del tamaño de la página
    page_width, page_height = pdf.pagesize
    available_width = page_width * 0.8 # Usar el 95% del ancho de la página
    column_width = available_width / len(column_names)

    # Crear la tabla en el PDF
    table_data = []
    for row in data:
        table_row = []
        for item in row:
            # Ajustar el contenido de las celdas si es demasiado largo
            adjusted_item = item[:50] + '...' if len(item) > 50 else item
            table_row.append(Paragraph(adjusted_item, styles['TableStyle']))
        table_data.append(table_row)

    table = Table(table_data, colWidths=[column_width] * len(column_names))

    # Configurar estilos para la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Fondo gris para la fila de encabezado
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para la fila de encabezado
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear el texto a la izquierda
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para la fila de encabezado
                        ('FONTSIZE', (0, 0), (-1, -1), font_size),  # Aplicar el tamaño de fuente reducido
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Relleno inferior para la fila de encabezado
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para las demás filas
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de cuadrícula negras
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinear el contenido de las celdas en la parte superior
                        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reducir el relleno izquierdo
                        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Reducir el relleno derecho
                        ('TOPPADDING', (0, 0), (-1, -1), 2)])  # Reducir el relleno superior
    table.setStyle(style)

    # Construir el PDF
    pdf.build([title_paragraph, Spacer(1, 0.2 * inch), date_paragraph, Spacer(1, 0.5 * inch), table])

    # Obtener el contenido del PDF como un HttpResponse
    pdf_response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'attachment; filename=Reporte.pdf'

    return pdf_response


def recover(request):
    return render(request, 'recover.html')

def model_update(request, pk):
    model = get_object_or_404(MyModel, pk=pk)
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES, instance=model)
        cambio_form = CambioCustodioForm(request.POST)
        if form.is_valid() and cambio_form.is_valid():
            model = form.save(commit=False)
            
            # Asignación y guardado del código TIC
            model.codigo_tic = request.POST.get('codigo_tic', '')  # Asegúrate de obtener el valor del campo código TIC correctamente

            # Ejemplo de asignación de archivo
            if 'archivo' in request.FILES:
                model.archivo = request.FILES['archivo']
            
            model.save()

            # Verificar si ya existe un objeto CambioCustodio para este modelo
            cambio = model.cambiocustodio_set.first()
            if not cambio:
                cambio = CambioCustodio(modelo_relacionado=model)
            cambio.nuevo_custodio = cambio_form.cleaned_data['nuevo_custodio']
            cambio.cedula_nuevo_custodio = cambio_form.cleaned_data['cedula_nuevo_custodio']
            cambio.fecha_cambio = timezone.now()  # Asigna la fecha actual
            cambio.save()

            messages.success(request, '¡Modelo actualizado correctamente!')
            return redirect('model_list')  # Redirige a donde quieras después de actualizar el modelo
    else:
        form = MyModelForm(instance=model)
        cambio_form = CambioCustodioForm()

    return render(request, 'actualizar.html', {'form': form, 'cambio_custodio_form': cambio_form, 'model': model})