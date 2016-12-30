# encoding:utf-8
import codecs
import sys
import urllib2

from bs4 import BeautifulSoup


def extrae_datos_pagina():
    file = open('datos.txt', 'r')
    lines = file.readlines()

    for i in lines:
        data_bruto = eval(i)
        url = data_bruto[1]

        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            pelicula = soup.find('td', {"valign": "top"})
            pelicula = pelicula.find_all('td', {"valign": "top"})
            datos_pelicula = pelicula[2]

            img_src = datos_pelicula.find('img')['src']
            actores = ''
            genero = ''
            director = ''
            fecha = ''
            formato = ''
            tamanyo = ''
            descargas = ''
            anyo = ''
            for i in datos_pelicula.find_all('b'):

                if 'Actores' in i.text:
                    actores = str(i.next_sibling.encode("utf-8")).strip()
                if u'G\xe9nero:' in i.text:
                    genero = str(i.next_sibling.encode("utf-8")).strip()
                if 'Director:' in i.text:
                    director = str(i.next_sibling.encode("utf-8")).strip()
                if u'A\xf1o:' in i.text:
                    anyo = str(i.next_sibling.encode("utf-8")).strip()
                if 'Fecha:' in i.text:
                    fecha = str(i.next_sibling.encode("utf-8")).strip()
                if 'Formato:' in i.text:
                    formato = str(i.next_sibling.encode("utf-8")).strip()
                if u'Tama\xf1o:' in i.text:
                    tamanyo = str(i.next_sibling.encode("utf-8")).strip()
                if 'Total Descargas:' in i.text:
                    descargas = str(i.next_sibling.encode("utf-8")).strip()
            descripcion = datos_pelicula.find('div', align='justify')
            descripcion = descripcion.text.split('\n')[0]

            enlace_torrent = 'http://www.tumeURL.com/' + datos_pelicula.a['href']

            titulo = datos_pelicula.find('span', style='font-size:18px;')
            titulo = str(titulo.text.encode("utf-8")).strip()

            data = [titulo, img_src, actores, genero, director, descripcion, anyo, fecha, formato, tamanyo, descargas,
                    enlace_torrent]
            file_exito = open('file_exito.txt', 'a')
            file_exito.write(str(data) + '\n')
            file_exito.close()

        except:
            file_error = open('file_error.txt', 'a')
            file_error.write(i)
            file_error.close()

def download_final_data():
    file = open('datos2.txt', 'r')
    lines = file.readlines()

    for i in lines:
        data_bruto = eval(i)
        url = data_bruto[-1]

        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            pelicula = soup.find('td', {"valign": "top"})
            pelicula = pelicula.find_all('td', {"valign": "top"})
            datos_pelicula = pelicula[2]

            url_download = 'http://www.tumeURL.com' + str(datos_pelicula.find('a')['href'])

            data_bruto.append(url_download)
            file_exito = open('file_exito.txt', 'a')
            file_exito.write(str(data_bruto) + '\n')
            file_exito.close()

        except:
            file_error = open('file_error.txt', 'a')
            file_error.write(i)
            file_error.close()