from django.shortcuts import render, redirect
from .models import Ticket 
from datetime import datetime

def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

# para registrar los tickets
def registrarticket(request):
    asunto=request.POST['asunto']
    descripcion=request.POST['descripcion']
    departamento=request.POST['departamento']
    estado=request.POST['estado']
    fecha_str = request.POST.get('fecha')
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

    tickets = Ticket.objects.create(asunto=asunto, descripcion=descripcion, departamento=departamento, estado=estado, fecha=fecha)
    return redirect('ticket_list')

# para elistar los tickets
def edicionticket(request, id):
    tickets = Ticket.objects.get(id=id)
    data={
        'titulo':'edicionticket',
        'tickets':tickets
    }
    return render(request, "editarticket.html", {"ticket":tickets})

def editarticket(request, id):

    asunto=request.POST['asunto']
    descripcion=request.POST['descripcion']
    departamento=request.POST['departamento']
    estado=request.POST['estado']
    fecha_str = request.POST.get('fecha')
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    
    tickets = Ticket.objects.get(id=id)
    tickets.asunto = asunto
    tickets.descripcion = descripcion
    tickets.departamento = departamento
    tickets.estado = estado
    tickets.fecha = fecha
    tickets.save()

    return redirect('ticket_list')

# para eliminar ticket
def eliminarticket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.delete()

    return redirect('ticket_list')

