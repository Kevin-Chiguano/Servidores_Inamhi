from django.db import models
#librerias

class MyModel(models.Model):
    # Campos del modelo MyModel
    codigo_bien = models.CharField(max_length=50, verbose_name='Código Bien')
    codigo_anterior = models.CharField(max_length=50, verbose_name='Código Anterior', blank=True, null=True)
    codigo_provisional = models.CharField(max_length=50, verbose_name='Código Provisional', blank=True, null=True)
    codigo_nuevo = models.CharField(max_length=50, verbose_name='Código Nuevo', blank=True, null=True)
    nombre_bien = models.CharField(max_length=100, verbose_name='Nombre Bien')
    serie = models.CharField(max_length=50, verbose_name='Serie', blank=True, null=True)
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    color = models.CharField(max_length=50, verbose_name='Color')
    material = models.CharField(max_length=50, verbose_name='Material')
    estado = models.CharField(max_length=50, verbose_name='Estado')
    ubicacion = models.CharField(max_length=100, verbose_name='Ubicación')
    cedula = models.CharField(max_length=20, verbose_name='Cédula')
    custodio_actual = models.CharField(max_length=150, verbose_name='Custodio Actual')
    observacion = models.TextField(verbose_name='Observación', blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/', verbose_name='Archivo Adjunto', blank=True, null=True)
    estado_registro = models.BooleanField(default=True, verbose_name='Estado de Registro')
    codigo_tic = models.CharField(max_length=50, verbose_name='Código Tic', blank=True, null=True)


    def __str__(self):
        return self.codigo_bien

class CambioCustodio(models.Model):
    modelo_relacionado = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    nuevo_custodio = models.CharField(max_length=150, verbose_name='Nuevo Custodio')
    cedula_nuevo_custodio = models.CharField(max_length=20, verbose_name='Cédula Nuevo Custodio')
    fecha_cambio = models.DateField(verbose_name='Fecha de Cambio')

    def __str__(self):
        return f"Cambio de custodio para {self.modelo_relacionado.nombre_bien} el {self.fecha_cambio}"


class Meta:
        permissions = [
            ("view_mymodel", "Can view MyModel"),
            ("change_mymodel", "Can change MyModel"),
            ("delete_mymodel", "Can delete MyModel"),
        ]