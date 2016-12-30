# encoding: utf-8

import os
import sqlite3

from whoosh import index
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser


class whoosh_indice():
    def __init__(self, folder_indice_peliculas, ruta_bd):
        self.folder_indice_peliculas = folder_indice_peliculas
        self.ruta_db = ruta_bd

        if not os.path.isdir(self.folder_indice_peliculas):
            os.mkdir(self.folder_indice_peliculas)

    def get_info_film(self, base_datos, id_pelicula):

        buscar_actores = base_datos.execute('''SELECT actor_id FROM aplication_pelicula_actores WHERE pelicula_id=?''',
                                            (id_pelicula,))
        list_actores = []
        list_directores = []
        for actor in buscar_actores:
            actor_id = actor[0]
            nombre = base_datos.execute('''SELECT nombre FROM aplication_actor WHERE id=?''', (int(actor_id),))
            list_actores.append(nombre.fetchone()[0])
        actores = ','.join([x.strip() for x in list_actores])

        buscar_directores = base_datos.execute(
            '''SELECT director_id FROM aplication_pelicula_directores WHERE pelicula_id=?''', (id_pelicula,))
        for director in buscar_directores:
            director_id = director[0]
            nombre = base_datos.execute('''SELECT nombre FROM aplication_director WHERE id=?''', (int(director_id),))
            list_directores.append(nombre.fetchone()[0])
        directores = ','.join([x.strip() for x in list_directores])

        return (actores, directores)

    def crea_indice_peliculas(self):

        db = sqlite3.connect(self.ruta_db)

        schema = Schema(id=ID(stored=True), titulo=TEXT(stored=False), sipnosis=TEXT(stored=False),
                        duracion=NUMERIC(stored=False), anyo=NUMERIC(stored=False), director=KEYWORD(stored=False),
                        actores=KEYWORD(stored=False), valoracion=NUMERIC(stored=False), pais=ID(stored=False))
        ix = create_in(self.folder_indice_peliculas, schema)
        writer = ix.writer()

        rows = db.execute('''SELECT * FROM aplication_pelicula''')

        for row in rows:
            id_pelicula = row[0]
            titulo = row[1]
            sipnosis = row[-1]
            valoracion_media = float(row[3])
            anyo = int(row[5])
            duracion = int(row[6])
            pais = row[7]

            print [id_pelicula, titulo, sipnosis, valoracion_media, anyo, duracion, pais]

            actores, directores = self.get_info_film(base_datos=db, id_pelicula=id_pelicula)

            writer.add_document(id=unicode(id_pelicula), titulo=unicode(titulo.strip()), sipnosis=unicode(sipnosis),
                                duracion=duracion, anyo=anyo, director=unicode(directores.strip()),
                                actores=unicode(actores.strip()), valoracion=valoracion_media,
                                pais=unicode(pais.strip()))
        writer.commit()


class whoosh_busqueda():
    def __init__(self, folder_indice_peliculas, ruta_db):
        self.folder_indice_peliculas = folder_indice_peliculas
        self.ruta_db = ruta_db

        w_indice = whoosh_indice(folder_indice_peliculas=folder_indice_peliculas, ruta_bd=ruta_db)

        # Si el indice agenda no existe se crea
        if not index.exists_in(self.folder_indice_peliculas):
            w_indice.crea_indice_peliculas()

    def buscar_director(self):

        ix = index.open_dir(self.folder_indice_peliculas)

        with ix.searcher() as searcher:
            query = QueryParser('director', ix.schema).parse('Alejandro Amenábar')
            busqueda = searcher.search(query)
            for i in busqueda:
                print i
                return i
