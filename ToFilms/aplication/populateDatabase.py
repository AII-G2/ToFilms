# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from django.db import transaction
from aplication.models import Director,Actor,Pelicula,Torrent
from django.db.models import Count

def leer_fichero(file):
    f = open(file, "r")
    s = f.read()
    f.close()
    return s

def populateDatabase():
    populateActores()
    populateDirectores()
    populatePeliculas()
    populateTorrents()


@transaction.atomic
def populateActores():
    actores = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Actor.objects.all().delete()
    for a in actores:
        info_actores = eval(a)[11].split(",")
        for a1 in info_actores:
            actor = Actor(nombre=a1)
            actor.save()


@transaction.atomic
def populateDirectores():
    directores = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Director.objects.all().delete()
    for d in directores:
        info_directores = eval(d)[7].split(",")
        print info_directores
        for d1 in info_directores:
            director = Director(nombre=d1)
            director.save()

@transaction.atomic
def populatePeliculas():
    peliculas = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Pelicula.objects.all().delete()
    for p in peliculas:
        info_pelicula = eval(p)
        actores = eval(p)[11].split(",")
        directores = eval(p)[7].split(",")
        if info_pelicula[2]!='--' and info_pelicula[2]!='':
            valoracion_media = info_pelicula[2].replace(",",".")
        else:
            valoracion_media = 0
        if info_pelicula[5]!='':
            duracion = info_pelicula[5].split(" ")[0]
        else:
            duracion = 0
        if info_pelicula[3]!='':
            votaciones_totales = info_pelicula[3].replace(".","")
        else:
            votaciones_totales = 0
        pelicula = Pelicula(titulo= info_pelicula[0], url_imagen= info_pelicula[1], valoracion_media= valoracion_media,
                            votaciones_totales= votaciones_totales, anyo= info_pelicula[4], duracion= duracion,
                            pais= info_pelicula[6], guion= info_pelicula[8], musica= info_pelicula[9], fotografia=info_pelicula[10],
                            productora= info_pelicula[12], categoria=info_pelicula[13], sinopsis= info_pelicula[14])
        pelicula.save()

        for a in actores:
            actor = Actor.objects.filter(nombre=a)[0]
            pelicula.actores.add(actor)

        for d in directores:
            director = Director.objects.filter(nombre=d)[0]
            pelicula.directores.add(director)

@transaction.atomic()
def populateTorrents():
    torrents = leer_fichero("ignoredFiles/torrentsFinal.txt").splitlines()
    peliculas = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Torrent.objects.all().delete()
    for t in torrents:
        info_torrent = eval(t)
        for p in peliculas:
            if info_torrent[0] == eval(p)[15]:
                pelicula = Pelicula.objects.filter(titulo=eval(p)[0], anyo=eval(p)[4])[0]
        torrent = Torrent(url= info_torrent[0], calidad= info_torrent[1], pelicula= pelicula)
        torrent.save()
