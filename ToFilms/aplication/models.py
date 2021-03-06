from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Actor(models.Model):
    nombre = models.CharField(max_length=150)

    def __unicode__(self):
        return self.nombre

class Director(models.Model):
    nombre = models.CharField(max_length=150)

    def __unicode__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=150)
    url_imagen = models.URLField()
    valoracion_media = models.DecimalField(max_digits=3, decimal_places=2)
    votaciones_totales = models.IntegerField(default=0)
    anyo = models.IntegerField();
    duracion = models.IntegerField();
    pais = models.CharField(max_length=100)
    guion = models.CharField(max_length=100)
    musica = models.CharField(max_length=100)
    fotografia = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    sinopsis = models.TextField(blank=True, null=True)

    actores = models.ManyToManyField(Actor)
    directores = models.ManyToManyField(Director)

    def __unicode__(self):
        return self.titulo+" ("+str(self.anyo)+")"


class Torrent(models.Model):
    calidad = models.CharField(max_length=100)
    url = models.URLField()

    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return self.url+" "+self.calidad
