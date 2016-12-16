# encoding=utf8
import sys

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
            print  "Error al conectarse a la página"
            return None

    fichero = "pelicula"
    link = "http://www.filmaffinity.com/es/advsearch.php?stext="+titulo+"&stype[]=title&fromyear="+anyo+"&toyear="+anyo
    if abrir_url(link, fichero):
        l = extraer_lista(fichero)
    if l:
        soup = BeautifulSoup(l, 'html.parser')
        peliculas = soup.findAll("div", "movie-card movie-card-1")
        reparto = ""
        for p in peliculas:
            #print(p)
            # print "Poster: " + p.find("div", "mc-poster").img.get('src')
            # print "Titulo: " + p.find("div", "mc-title").a.string
            # print "Enlace: http://www.filmaffinity.com" + p.find("div", "mc-title").a.get('href')
            # print "País: http://www.filmaffinity.com" + p.find("div", "mc-title").img.get('src')
            # print "Rating: [valoracion = " + p.find("div", "mr-rating").find("div",
            #                                                                  "avgrat-box").string + ", usuarios = " + \
            #       p.find("div", "mr-rating").find("div", "ratcount-box").contents[0].string + "]"
            # print "Director: " + p.find("div", "mc-director").div.span.string
            # for r in p.find("div", "mc-cast").findAll("span", "nb"):
            #     # print "Actor: "+r.contents[0].string
            #     reparto = reparto + ", " + r.contents[0].string
            # print("Reparto: " + reparto)
            if director == p.find("div", "mc-director").div.span.string:
                titulo = p.find("div", "mc-title").a.string
                link = "http://www.filmaffinity.com"+p.find("div", "mc-title").a.get('href')
                poster = p.find("div","mc-poster").img.get('src')
                rating = p.find("div", "mr-rating").find("div","avgrat-box").string
                nvotos = p.find("div", "mr-rating").find("div","ratcount-box").contents[0].string
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
        productora = ""
        idguion = 0
        idmusica = 0
        idfotografia = 0
        idproductora = 0
        for p in info_pelicula.findAll("dt"):
            if "Música" in p.string:
                idmusica = idguion + 1
            if "Fotografía" in p.string:
                idfotografia = idguion+idmusica+1
            if "Productora" in p.string:
                idguion = idguion+idmusica+idfotografia+1
        fecha = info_pelicula.find("dd", {"itemprop": "datePublished"}).string
        #print "Fecha: "+fecha
        duracion = info_pelicula.find("dd", {"itemprop": "duration"}).string
        #print "Duracion: "+duracion
        pais = info_pelicula.find("span", {"id": "country-img"}).img.get('title')
        #print "Pais: "+pais
        for d in info_pelicula.find("dd", "directors").findAll("a"):
            director = director + d.get('title') + ", "
        director = director[0:len(director) - 2]
        #print "Director: " + director
        for g in info_pelicula.findAll("div", "credits")[0]:
            if len(re.findall(r'<span>(.*)</span>', str(g)))>0:
                guion = guion+" "+re.findall(r'<span>(.*)</span>', str(g))[0].replace("</span>","")
        #print "Guion: "+guion
        if idmusica!=0:
            for m in info_pelicula.findAll("div", "credits")[idmusica]:
                if len(re.findall(r'<span>(.*)</span>', str(m)))>0:
                    musica = musica+" "+re.findall(r'<span>(.*)</span>', str(m))[0].replace("</span>","")
            #print "Musica: "+musica
        if idfotografia!=0:
            for f in info_pelicula.findAll("div", "credits")[idfotografia]:
                if len(re.findall(r'<span>(.*)</span>', str(f)))>0:
                    fotografia = fotografia+" "+re.findall(r'<span>(.*)</span>', str(f))[0].replace("</span>","")
            #print "Fotografia: "+fotografia
        for a in info_pelicula.findAll("span", {"itemprop": "name"}):
            actores = actores+a.string+", "
        actores = actores[0:len(actores)-2]
        #print "Reparto: "+actores
        if idproductora!=0:
            for p in info_pelicula.findAll("div", "credits")[idproductora]:
                if len(re.findall(r'<span>(.*)</span>', str(p)))>0:
                    productora = productora+" "+re.findall(r'<span>(.*)</span>', str(p))[0].replace("</span>","")
            #print "Productora: "+productora
        genero = info_pelicula.find("span", {"itemprop": "genre"}).a.string
        #print "Género: "+genero
        sipnosis = info_pelicula.find("dd", {"itemprop": "description"}).string
        #print "Sipnosis: "+sipnosis

    return [titulo, poster, rating, nvotos, fecha, duracion, pais, director, guion, musica, fotografia, actores, productora, genero, sipnosis]


def extraer_lista(file):
    f = open(file, "r")
    l = f.read()
    f.close()
    return l

torrents = extraer_lista("../../ignoredFiles/torrents.txt")
i = 0
printProgress(i, 14165, prefix='Progress:', suffix='Complete', barLength=50)
count = 0
for t in torrents.splitlines():
    # print eval(t)
    # print eval(t)[0]
    # print eval(t)[4][3:].replace(".","")
    # print eval(t)[6][3:]
    try:
        extraer_peliculas(eval(t)[0], eval(t)[4][3:].replace(".",""), eval(t)[6][3:].replace(".",""))
    except Exception:
        #print eval(t)[0]
        count = count + 1
        #print count
    printProgress(i, 14165, prefix='Progress:', suffix='Complete', barLength=50)
    i = i + 1

print i
