# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import urllib, re
from bs4 import BeautifulSoup

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
        # for p in info_pelicula:
        #     print p
        fecha = info_pelicula.find("dd", {"itemprop": "datePublished"}).string
        print "Fecha: "+fecha
        duracion = info_pelicula.find("dd", {"itemprop": "duration"}).string
        print "Duracion: "+duracion
        pais = info_pelicula.find("span", {"id": "country-img"}).img.get('title')
        print "Pais: "+pais
        for d in info_pelicula.find("dd", "directors").findAll("a"):
            director = director + d.get('title') + ", "
        director = director[0:len(director) - 2]
        print "Director: " + director
        for g in info_pelicula.findAll("div", "credits")[0]:
            if len(re.findall(r'<span>(.*)</span>', str(g)))>0:
                guion = guion+" "+re.findall(r'<span>(.*)</span>', str(g))[0].replace("</span>","")
        print "Guion: "+guion
        for m in info_pelicula.findAll("div", "credits")[1]:
            if len(re.findall(r'<span>(.*)</span>', str(m)))>0:
                musica = musica+" "+re.findall(r'<span>(.*)</span>', str(m))[0].replace("</span>","")
        print "Musica: "+musica
        for f in info_pelicula.findAll("div", "credits")[2]:
            if len(re.findall(r'<span>(.*)</span>', str(f)))>0:
                fotografia = fotografia+" "+re.findall(r'<span>(.*)</span>', str(f))[0].replace("</span>","")
        print "Fotografia: "+fotografia
        for a in info_pelicula.findAll("span", {"itemprop": "name"}):
            actores = actores+a.string+", "
        actores = actores[0:len(actores)-2]
        print "Reparto: "+actores
        for p in info_pelicula.findAll("div", "credits")[3]:
            if len(re.findall(r'<span>(.*)</span>', str(p)))>0:
                productora = productora+" "+re.findall(r'<span>(.*)</span>', str(p))[0].replace("</span>","")
        print "Productora: "+productora
        genero = info_pelicula.find("span", {"itemprop": "genre"}).a.string
        print "Género: "+genero
        sipnosis = info_pelicula.find("dd", {"itemprop": "description"}).string
        print "Sipnosis: "+sipnosis

    return [titulo, poster, rating, nvotos, fecha, duracion, pais, director, guion, musica, fotografia, actores, productora, genero, sipnosis]

print extraer_peliculas("Titanic", "James Cameron", "1997")