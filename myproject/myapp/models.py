from django.db import models

class MyModel(models.Model):
    # Campos del modelo MyModel
    DireccionIp = models.CharField(max_length=200, verbose_name='DireccionIp', blank=True, null=True)
    Usuario = models.CharField(max_length=100, verbose_name='Usuario', blank=True, null=True)
    Contrasena = models.CharField(max_length=50, verbose_name='Contrasena', blank=True, null=True)
    Servicio = models.CharField(max_length=100, verbose_name='Servicio', blank=True, null=True)
    Puerto = models.CharField(max_length=25, verbose_name='Puerto', blank=True, null=True)
    RutaImportante = models.CharField(max_length=100, verbose_name='RutaImportante', blank=True, null=True)
    UbicacionFisica = models.CharField(max_length=250, verbose_name='UbicacionFisica', blank=True, null=True)
    NumeroSerie = models.CharField(max_length=50, verbose_name='Serie/Modelo', blank=True, null=True)


    def __str__(self):
        return self.DireccionIp
    
    class Meta:
        permissions = [
            ("view_custom_mymodel", "Can view MyModel"),
            ("edit_custom_mymodel", "Can edit MyModel"),
            ("remove_custom_mymodel", "Can remove MyModel"),
        ]