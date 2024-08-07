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
from .models import Nodos
from .forms import NodosForm
from .forms import MyModelForm, CustomUserCreationForm
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
    return render(request, 'model_detail.html', {'model': model})

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_list(request):
    models = Servidores.objects.all()
    return render(request, 'model_list.html', {'models': models})

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
        model.save()
        return redirect('model_list')
    return redirect('model_confirm_delete', pk=pk)

@login_required
@permission_required('myapp.view_mymodel', raise_exception=True)
def model_confirm_delete(request, pk):
    model = get_object_or_404(Servidores, pk=pk)
    return render(request, 'model_confirm_delete.html', {'model': model})

@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')

@login_required
def salir(request):
    logout(request)
    return redirect('/')

# Exportación a Excel
def export_to_excel(request):
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
        ws.append([obj.NombreServidor, obj.Marca, obj.Modelo, obj.SistemaOperativo, obj.Entorno, obj.Estado, 
                   obj.direccionIpPublica, obj.DireccionIpLocal, obj.Usuario, obj.Contrasena, obj.Servicio, obj.Puerto, obj.RutaImportante, obj.UbicacionFisica, obj.NumeroSerie, obj.DescripcionProcesos])

    # Crear una respuesta de HTTP con el archivo adjunto
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte.xlsx'
    wb.save(response)
    return response

def export_to_pdf(request):
    queryset = Servidores.objects.all()

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
    column_names = ['DireccionIp', 'Usuario', 'Contrasena', 'Servicio', 'Puerto', 'RutaImportante', 
                    'UbicacionFisica', 'NumeroSerie']
    data.append(column_names)

    # Obtener los valores de los campos para cada objeto en queryset
    for item in queryset:
        row = [item.DireccionIp, item.Usuario, item.Contrasena, item.Servicio, item.Puerto, item.RutaImportante, 
               item.UbicacionFisica, item.NumeroSerie]
        data.append(row)

    # Calcular el ancho de la tabla en función del tamaño de la página
    page_width, page_height = pdf.pagesize
    available_width = page_width * 0.8 # Usar el 80% del ancho de la página
    column_width = available_width / len(column_names)

    # Crear la tabla en el PDF
    table_data = []
    for row in data:
        table_row = [Paragraph(item[:50] + '...' if len(item) > 50 else item, styles['TableStyle']) for item in row]
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


#Nodo ------------------------------------------------------------------------
@login_required
@permission_required('myapp.view_nodos', raise_exception=True)
def nodos_list(request):
    nodos = Nodos.objects.all()
    return render(request, 'nodos/nodos_list.html', {'nodos': nodos})

@login_required
@permission_required('myapp.add_nodos', raise_exception=True)
def nodos_create(request):
    if request.method == 'POST':
        form = NodosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nodos_list')
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
            return redirect('nodos_list')
    else:
        form = NodosForm(instance=nodo)
    return render(request, 'nodos/nodos_form.html', {'form': form, 'nodo': nodo})

@login_required
@permission_required('myapp.delete_nodos', raise_exception=True)
def nodos_delete(request, pk):
    nodo = get_object_or_404(Nodos, pk=pk)
    if request.method == 'POST':
        nodo.delete()
        return redirect('nodos_list')
    return render(request, 'nodos/nodos_confirm_delete.html', {'nodo': nodo})

@login_required
@permission_required('myapp.view_nodos', raise_exception=True)
def nodos_detail(request, pk):
    nodo = get_object_or_404(Nodos, pk=pk)
    return render(request, 'nodos/nodos_detail.html', {'nodo': nodo})