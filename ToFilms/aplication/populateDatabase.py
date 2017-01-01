# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from django.db import transaction
from aplication.models import Director,Actor,Pelicula,Torrent
from django.db.models import Count

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

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
    print "Populando Actores"
    i = 0
    actores = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Actor.objects.all().delete()
    printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)
    for a in actores:
        info_actores = eval(a)[11].split(",")
        for a1 in info_actores:
            Actor.objects.get_or_create(nombre=a1)
        i = i + 1
        printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)


@transaction.atomic
def populateDirectores():
    print "Populando Directores"
    directores = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Director.objects.all().delete()
    i = 0
    printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)
    for d in directores:
        info_directores = eval(d)[7].split(",")
        print info_directores
        for d1 in info_directores:
            Director.objects.get_or_create(nombre=d1)
        i = i + 1
        printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)

@transaction.atomic()
def populateTorrents():
    print "Populando Torrents"
    torrents = leer_fichero("ignoredFiles/torrentsFinal.txt").splitlines()
    Torrent.objects.all().delete()
    i = 0
    printProgress(i, 14169, prefix='Progress:', suffix='Complete', barLength=50)
    for t in torrents:
        info_torrent = eval(t)
        torrent = Torrent(url= info_torrent[0], calidad= info_torrent[1])
        torrent.save()
        i = i + 1
        printProgress(i, 14169, prefix='Progress:', suffix='Complete', barLength=50)

@transaction.atomic
def populatePeliculas():
    print "Populando Peliculas"
    peliculas = leer_fichero("ignoredFiles/peliculasFinal").splitlines()
    Pelicula.objects.all().delete()
    i = 0
    printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)
    for p in peliculas:
        info_pelicula = eval(p)
        actores = info_pelicula[11].split(",")
        directores = info_pelicula[7].split(",")
        torrents = info_pelicula[14].split(",")
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
        Pelicula.objects.get_or_create(titulo= info_pelicula[0], url_imagen= info_pelicula[1],
                            valoracion_media= valoracion_media, anyo= info_pelicula[4], duracion= duracion,
                            pais= info_pelicula[6], guion= info_pelicula[8], musica= info_pelicula[9], fotografia=info_pelicula[10],
                            categoria=info_pelicula[12], sinopsis= info_pelicula[13])
        pelicula = Pelicula.objects.get(titulo= info_pelicula[0], url_imagen= info_pelicula[1],
                            valoracion_media= valoracion_media, anyo= info_pelicula[4], duracion= duracion,
                            pais= info_pelicula[6], guion= info_pelicula[8], musica= info_pelicula[9], fotografia=info_pelicula[10],
                            categoria=info_pelicula[12], sinopsis= info_pelicula[13])

        pelicula.votaciones_totales = votaciones_totales
        pelicula.save()

        for a in actores:
            actor = Actor.objects.filter(nombre=a)[0]
            pelicula.actores.add(actor)

        for d in directores:
            director = Director.objects.filter(nombre=d)[0]
            pelicula.directores.add(director)

        for t in torrents:
            try:
                torrent = Torrent.objects.filter(url=t)[0]
                pelicula.torrent_set.add(torrent)
            except:
                print t

        i = i + 1
        printProgress(i, 8154, prefix='Progress:', suffix='Complete', barLength=50)
