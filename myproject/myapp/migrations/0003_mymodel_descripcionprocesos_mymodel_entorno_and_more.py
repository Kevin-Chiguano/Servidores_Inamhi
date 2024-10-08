# Generated by Django 5.0.6 on 2024-08-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_mymodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='DescripcionProcesos',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='DescripcionProcesos'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='Entorno',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Entorno'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='Estado',
            field=models.BooleanField(blank=True, max_length=100, null=True, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='Marca',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Marca'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='Modelo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Modelo'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='NombreServidor',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nombreServidor'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='SistemaOperativo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='SistemaOperativo'),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='direccionIpPublica',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='DireccionIpPublica'),
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='DireccionIp',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='DireccionIp'),
        ),
    ]
