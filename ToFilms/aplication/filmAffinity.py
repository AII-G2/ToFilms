# encoding=utf8
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

import urllib, re
from bs4 import BeautifulSoup

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

def extraer_peliculas(titulo, director, anyo):
    def extraer_lista(file):
        f = open(file, "r")
        l = f.read()
        f.close()
        return l

    def abrir_url(url, file):
        try:
            f = urllib.urlretrieve(url, file)
            return file
        except:
            print("Error al conectarse a la página")
            return None

    fichero = "pelicula"
    link = "http://www.filmaffinity.com/es/advsearch.php?stext="+titulo+"&stype[]=title&fromyear="+anyo+"&toyear="+anyo
    if abrir_url(link, fichero):
        l = extraer_lista(fichero)
    if l:
        soup = BeautifulSoup(l, 'html.parser')
        peliculas = soup.findAll("div", "movie-card movie-card-1")
        directorPelicula = ""
        for p in peliculas:
            for g in p.find("div", "mc-director").div.findAll("span","nb"):
                if director!="":
                    directorPelicula = directorPelicula+", "+g.a.get('title')
                else:
                    directorPelicula = g.a.get('title')
            if director in directorPelicula:
                titulo = p.find("div", "mc-title").a.string
                link = "http://www.filmaffinity.com"+p.find("div", "mc-title").a.get('href')
                poster = p.find("div","mc-poster").img.get('src')
                rating = p.find("div", "mr-rating").find("div","avgrat-box").string
                try:
                    nvotos = p.find("div", "mr-rating").find("div","ratcount-box").contents[0].string
                except:
                    nvotos = ""
                info_peliculas = extraer_info_peliculas(titulo, link, poster, rating, nvotos)
                break

    return info_peliculas

def extraer_info_peliculas(titulo, link, poster, rating, nvotos):
    def extraer_lista(file):
        f = open(file, "r")
        l = f.read()
        f.close()
        return l

    def abrir_url(url, file):
        try:
            f = urllib.urlretrieve(url, file)
            return file
        except:
            print  "Error al conectarse a la página"
            return None

    fichero = "info_pelicula"
    link = link
    if abrir_url(link, fichero):
        l = extraer_lista(fichero)
    if l:
        soup = BeautifulSoup(l, 'html.parser')
        info_pelicula = soup.find("div", "z-movie").find("div", {"id": "left-column"}).find("dl", "movie-info")
        actores = ""
        director = ""
        fotografia = ""
        guion = ""
        musica = ""
        idguion = 0
        idmusica = 0
        idfotografia = 0
        for p in info_pelicula.findAll("dt"):
            if "Música" in p.string:
                idmusica = idguion + 1
            if "Fotografía" in p.string:
                idfotografia = idguion+idmusica+1
        fecha = info_pelicula.find("dd", {"itemprop": "datePublished"}).string
        try:
            duracion = info_pelicula.find("dd", {"itemprop": "duration"}).string
        except:
            duracion = ""
        pais = info_pelicula.find("span", {"id": "country-img"}).img.get('title')
        for d in info_pelicula.find("dd", "directors").findAll("a"):
            director = director + d.get('title') + ", "
        director = director[0:len(director) - 2]
        try:
            for g in info_pelicula.findAll("div", "credits")[0]:
                if len(re.findall(r'<span>(.*)</span>', str(g)))>0:
                    guion = guion+" "+re.findall(r'<span>(.*)</span>', str(g))[0].replace("</span>","")
        except:
            guion = ""
        if idmusica!=0:
            try:
                for m in info_pelicula.findAll("div", "credits")[idmusica]:
                    if len(re.findall(r'<span>(.*)</span>', str(m)))>0:
                        musica = musica+" "+re.findall(r'<span>(.*)</span>', str(m))[0].replace("</span>","")
            except:
                musica=""
        if idfotografia!=0:
            try:
                for f in info_pelicula.findAll("div", "credits")[idfotografia]:
                    if len(re.findall(r'<span>(.*)</span>', str(f)))>0:
                        fotografia = fotografia+" "+re.findall(r'<span>(.*)</span>', str(f))[0].replace("</span>","")
            except:
                fotografia = ""
        for a in info_pelicula.findAll("span", {"itemprop": "name"}):
            actores = actores+a.string+", "
        actores = actores[len(director)+2:len(actores)-2]
        genero = info_pelicula.find("span", {"itemprop": "genre"}).a.string
        try:
            sipnosis = info_pelicula.find("dd", {"itemprop": "description"}).string
        except:
            sipnosis = ""

    return [titulo, poster, rating, nvotos, fecha, duracion, pais, director, guion, musica, fotografia, actores, genero, sipnosis]


def extraer_lista(file):
    f = open(file, "r")
    l = f.read()
    f.close()
    return l

torrents = extraer_lista("../ignoredFiles/torrents1.txt")
i = 11786
printProgress(i, 14165, prefix='Progress:', suffix='Complete', barLength=50)
count = 0
f = open("../../ignoredFiles/peliculas", "a")
torrentsArray = torrents.splitlines()

for t in range(11786,len(torrentsArray)):
    time.sleep(5)
    titulo = eval(torrentsArray[t])[0]
    director = eval(torrentsArray[t])[4][3:].replace(".","")
    anyo = eval(torrentsArray[t])[6][3:].replace(".","")
    try:
        extraccion = extraer_peliculas(titulo, director, anyo)
        f.write(str(extraccion))
        f.write("\n")
    except UnboundLocalError:
        count = count + 1
    printProgress(i, 14165, prefix='Progress:', suffix='Complete', barLength=50)
    i = i + 1

f.close()
print(count)

# Eliminación de Películas repetidas y se le añade un torrent por defecto

peliculas = extraer_lista("../ignoredFiles/peliculas1").splitlines()
f = open("../ignoredFiles/peliculasFinal", "a")
i = 0
peliculasSet = set()
printProgress(i, 11546, prefix='Progress:', suffix='Complete', barLength=50)
for p in range(0,len(peliculas)):
    temp = eval(peliculas[p])
    temp.append('')
    peliculasSet.add(str(temp))
    printProgress(i, 11546, prefix='Progress:', suffix='Complete', barLength=50)
    i = i + 1
for p in peliculasSet:
    f.write(p)
    f.write("\n")
f.close()

#Se le añaden los link de los torrents a las películas

torrentsArray = extraer_lista("../ignoredFiles/torrents.txt").splitlines()
peliculas = extraer_lista("../ignoredFiles/peliculas1").splitlines()
f = open("../ignoredFiles/peliculasFinal", "a")
i = 0

printProgress(i, 8524, prefix='Progress:', suffix='Complete', barLength=50)
for p in peliculas:
    pelicula = eval(p)
    torrents = ''
    for t in torrentsArray:
        torrent = eval(t)
        if pelicula[7] in torrent[4][3:].replace(".", "") and pelicula[4] in torrent[6][3:]:
            if torrents=='':
                torrents = torrent[len(torrent)-1]
            else:
                torrents = torrents+", "+torrent[len(torrent)-1]
    pelicula[len(pelicula)-1] = torrents
    f.write(str(pelicula))
    f.write("\n")
    printProgress(i, 8524, prefix='Progress:', suffix='Complete', barLength=50)
    i = i + 1
f.close()

#Se crea un fichero con los links de los torrents y su calidad


torrentsArray = extraer_lista("../ignoredFiles/torrents.txt").splitlines()
peliculas = extraer_lista("../ignoredFiles/peliculasFinal").splitlines()
f = open("../ignoredFiles/torrentsFinal.txt", "a")
i = 0

printProgress(i, 8524, prefix='Progress:', suffix='Complete', barLength=50)
for p in peliculas:
    pelicula = eval(p)
    if "," in pelicula[len(pelicula)-1]:
        urls = pelicula[len(pelicula)-1].split(",")
    else:
        urls = [pelicula[len(pelicula)-1]]
    for u in urls:
        for t in torrentsArray:
            torrent = eval(t)
            if torrent[len(torrent)-1] in u:
                f.write(str([u,torrent[8]]))
                f.write("\n")
                break
    printProgress(i, 8524, prefix='Progress:', suffix='Complete', barLength=50)
    i = i + 1
f.close()