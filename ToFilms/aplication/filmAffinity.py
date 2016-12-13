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
                extraer_info_peliculas(link, poster, rating, nvotos)
                break

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
        info_pelicula = soup.find("div", "z-movie").find("div", { "id" : "left-column" }).find("dl", "movie-info")
        print "Fecha: "
        print "Duracion: "
        print "Pais: "
        print "Director: "
        print "Guion: "
        print "Musica: "
        print "Fotografia: "
        print "Reparto: "
        print "Productora: "
        print "Género: "
        print "Sipnosis: "


extraer_peliculas("Titanic", "James Cameron", "1997")