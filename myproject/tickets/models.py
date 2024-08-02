from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now

class Ticket(models.Model):
    # llave primaria
    titulo = models.CharField(max_length=200, verbose_name='titulo')
    asunto = models.TextField(max_length=100, verbose_name='asunto')
    descripcion = models.TextField(max_length=200, verbose_name='descipcion')
    departamento = models.TextField(max_length=200, verbose_name='departamento')
    estado = models.CharField(max_length=200, verbose_name='estado')
    fecha = models.DateTimeField(default=now, verbose_name='fecha')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   # Otros campos que puedas necesitar...

def __str__(self):
    texto = "{0} ({7})"
    return texto.formats(self.titulo, self.asunto, self.descripcion, self.departamento, self.estado, self.fecha) 

