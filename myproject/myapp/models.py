from django.db import models

class Servidores(models.Model):
    # Campos del modelo MyModel
    DireccionIp = models.CharField(max_length=100, verbose_name='DireccionIp', blank=True, null=True)
    Usuario = models.CharField(max_length=100, verbose_name='Usuario', blank=True, null=True)
    Contrasena = models.CharField(max_length=50, verbose_name='Contrasena', blank=True, null=True)
    Servicio = models.CharField(max_length=100, verbose_name='Servicio', blank=True, null=True)
    Puerto = models.CharField(max_length=25, verbose_name='Puerto', blank=True, null=True)
    RutaImportante = models.CharField(max_length=100, verbose_name='RutaImportante', blank=True, null=True)
    UbicacionFisica = models.CharField(max_length=250, verbose_name='UbicacionFisica', blank=True, null=True)
    NumeroSerie = models.CharField(max_length=50, verbose_name='Serie/Modelo', blank=True, null=True)

    def __str__(self):
        return self.DireccionIp
    
class ApisYsubdominios(models.Model):
    NombreServicioHttps = models.CharField(max_length=150, verbose_name='Nombre Servicio HTTPS', blank=True, null=True)
    Descripcion = models.CharField(max_length=250, verbose_name='Descripción', blank=True, null=True)
    Ip = models.CharField(max_length=100, verbose_name='IP', blank=True, null=True)
    puerto = models.CharField(max_length=50, verbose_name='Puerto', blank=True, null=True)

    def __str__(self):
        return self.NombreServicioHttps

    
class Subdominios(models.Model):
    Nombre = models.CharField(max_length=100, verbose_name='Nombre', blank=True, null=True)
    IpPublica = models.CharField(max_length=100, verbose_name='IpPublica', blank=True, null=True)
    IpInterna = models.CharField(max_length=100, verbose_name='IpInterna', blank=True, null=True)
    Host = models.CharField(max_length=100, verbose_name='Host', blank=True, null=True)

    def __str__(self):
        return self.Nombre

class Nodos(models.Model):
    Host = models.CharField(max_length=100, verbose_name='Host', blank=True, null=True)
    Usuario = models.CharField(max_length=50, verbose_name='Usuario', blank=True, null=True)
    Ram = models.CharField(max_length=25, verbose_name='Ram', blank=True, null=True)
    Disco = models.CharField(max_length=25, verbose_name='Disco', blank=True, null=True)
    SistemaOperativo = models.CharField(max_length=50, verbose_name='SkistemaOperativo', blank=True, null=True)
    Descripcion = models.CharField(max_length=100, verbose_name='Descripcion', blank=True, null=True)
    Contrasena = models.CharField(max_length=50, verbose_name='contrasena', blank=True, null=True)

    def __str__(self):
        return self.Usuario

class Formulario(models.Model):
    NombreServidor = models.CharField(max_length=50, verbose_name='NombreServidor', blank=True, null=True)
    Ubicacion = models.CharField(max_length=150, verbose_name='Ubicacion', blank=True, null=True)
    Marca = models.CharField(max_length=50, verbose_name='Marca', blank=True, null=True)
    Modelo = models.CharField(max_length=50, verbose_name='Modelo', blank=True, null=True)
    NumeroSerie = models.CharField(max_length=25, verbose_name='NumeroSerie', blank=True, null=True)
    SistemaOperativo = models.CharField(max_length=50, verbose_name='SistemaOperativo', blank=True, null=True)
    PuertoRelevante = models.CharField(max_length=50, verbose_name='PuertoRelevante', blank=True, null=True)
    Entorno = models.CharField(max_length=50, verbose_name='Entorno', blank=True, null=True)
    Estado = models.BooleanField(max_length=15, verbose_name='Estado', blank=True, null=True)
    DireccionIpLocal = models.CharField(max_length=50, verbose_name='DireccionIpLocal', blank=True, null=True)
    DireccionIpPublica = models.CharField(max_length=50, verbose_name='DireccionIpPublica', blank=True, null=True)
    Usuario = models.CharField(max_length=25, verbose_name='Usuario', blank=True, null=True)
    Clave = models.CharField(max_length=25, verbose_name='Clave', blank=True, null=True)
    DescripcionProcesos = models.CharField(max_length=100, verbose_name='DescripcionProcesos', blank=True, null=True)

    def __str__(self):
        return self.NombreServidor
    
    
    class Meta:
        permissions = [
            ("view_custom_mymodel", "Can view MyModel"),
            ("edit_custom_mymodel", "Can edit MyModel"),
            ("remove_custom_mymodel", "Can remove MyModel"),
        ]