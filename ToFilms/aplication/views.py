# coding=utf-8

from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import render_to_response

from aplication.models import Pelicula, Torrent
from forms import PeliculaForm, PuntuacionForm


# Create your views here.
def principal(request):
    if request.method == 'POST':
        formulario = PeliculaForm(request.POST)
        if formulario.is_valid():
            tituloDePelicula = formulario.cleaned_data['Busqueda']
            message = ""
            peliculas = Pelicula.objects.filter(titulo__contains=tituloDePelicula)
            numResultados = len(peliculas)
            if len(peliculas) == 0:
                message = "No se han encontrado resultados"
            # Inicio el paginador
            pag = Paginate(request, peliculas, 5)

            # Contexto a retornar a la vista
            cxt = {
                'posts': pag['queryset'],
                'totPost': peliculas,
                'paginator': pag
            }
            return render_to_response('peliculas.html',
                                      {'peliculas': cxt, 'message': message, 'tituloDePelicula': tituloDePelicula, 'numResultados':numResultados})
    else:
        formulario = PeliculaForm()
        numPeliculas = Pelicula.objects.all().count()
        return render(request, 'principal.html', {'formulario': formulario, 'numPeliculas': numPeliculas})


def Paginate(request, queryset, pages):
    """
    PARAMETROS:
    request: Request de la vista
    queryset: Queryset a utilizar en la paginación
    pages: Cantidad de paginas del paginador
    """
    # Retorna el objeto paginator para comenzar el trabajo
    result_list = Paginator(queryset, pages)

    try:
        # Tomamos el valor de parametro page, usando GET
        page = int(request.GET.get('page'))
    except:
        page = 1

    # Si es menor o igual a 0 igualo en 1
    if page <= 0:
        page = 1

    # Si viene un parámetro que es mayor a la cantidad
    # de paginas le igualo el parámetro con las cant de paginas
    if (page > result_list.num_pages):
        page = result_list.num_pages

    # Verificamos si esta dentro del rango
    if (result_list.num_pages >= page):
        # Obtengo el listado correspondiente al page
        pagina = result_list.page(page)

        context = {
            'queryset': pagina.object_list,
            'page': page,
            'pages': result_list.num_pages,
            'has_next': pagina.has_next(),
            'has_prev': pagina.has_previous(),
            'next_page': page + 1,
            'prev_page': page - 1,
            'firstPage': 1,
        }

    return context


def mostrar_peliculas(request):
    try:
        # Tomamos el valor de parametro page, usando GET
        tituloDePelicula = request.GET.get('film')

        peliculas = Pelicula.objects.filter(titulo__contains=tituloDePelicula)
        numResultados = len(peliculas)
    except:
        print("ERROR")

    # Inicio el paginador
    pag = Paginate(request, peliculas, 5)

    # Contexto a retornar a la vista
    cxt = {
        'posts': pag['queryset'],
        'totPost': peliculas,
        'paginator': pag
    }
    return render(request, 'peliculas.html', {'peliculas': cxt, 'tituloDePelicula': tituloDePelicula, 'numResultados': numResultados})


def item_page(request):
    try:
        # Tomamos el valor de parametro page, usando GET
        idP = request.GET.get('film')
        pelicula = Pelicula.objects.get(id=idP)
        torrents = Torrent.objects.filter(pelicula=pelicula)

        actoresPelicula = pelicula.actores.values_list('nombre', flat=True)
        ultimoActorPelicula = actoresPelicula[len(actoresPelicula) - 1]

        directoresPelicula = pelicula.directores.values_list('nombre', flat=True)
        ultimoDirectoresPelicula = directoresPelicula[len(directoresPelicula) - 1]

    except:
        item = None
        pelicula = None

    return render(request, 'item_page.html',
                  {'pelicula': pelicula, 'torrents': torrents, 'ultimoActorPelicula': ultimoActorPelicula,
                   'ultimoDirectoresPelicula': ultimoDirectoresPelicula})


def about_toFilms(request):
    message = 'toFilms es un proyecto pensado y propuesto para la asignatura de Acceso Inteligente a la Información, ' \
              'con el que se ha conseguido relacionar peliculas del portal "www.filmaffinity.com" con archivos de descarga torrents ' \
              'del portal "www.mejortorrent.com", de manera que tenemos para cada una de las peliculas una serie de links de descarga' \
              ' para poder descargar. Equipo de desarrollo:' \

    return render(request, 'about.html', {'message': message})


def busqueda_avanzada(request):
    from aplication.busqueda.busquedaWhoosh import buscar

    if request.method == 'POST':
        formulario = PuntuacionForm(request.POST)
        datos = {}
        array_url = []
        valores = ['titulo']

        for i in formulario:
            nombre = i.name
            valor = i.value().encode('utf-8')
            if len(valor) > 0:
                array_url.append(nombre + '=' + valor)
                datos[nombre] = valor

        # Llamamos la clase buscar y le pasamos los datos para que busque
        # crea_indice_peliculas(db_path='.//db.sqlite3',path='aplication//busqueda//indexfilms')
        busqueda = buscar(path_index='aplication//busqueda//indexfilms', datos=datos)
        peliculas = Pelicula.objects.filter(id__in=busqueda)

        if len(peliculas) == 0:
            message = "No se han encontrado resultados"
        # Inicio el paginador
        pag = Paginate(request, peliculas, 5)

        # Contexto a retornar a la vista
        cxt = {
            'posts': pag['queryset'],
            'totPost': peliculas,
            'paginator': pag
        }
        url_string = '&'.join(x for x in array_url)

        return render(request, 'busqueda_whoosh.html',
                      {'formulario': formulario, 'peliculas': cxt, 'url': url_string,'datos': datos})
    else:
        formulario = PuntuacionForm()
        valores = ['titulo', 'sipnosis', 'actores', 'director', 'anyo', 'valoracion', 'pais', 'duracion']
        datos = {}
        array_url = []
        for valor in valores:
            try:
                dato = request.GET.get(valor).encode('utf-8')
                array_url.append(valor + '=' + dato)
                datos[valor] = dato
            except:
                pass
        if len(datos) > 0:
            busqueda = buscar(path_index='aplication//busqueda//indexfilms', datos=datos)
            peliculas = Pelicula.objects.filter(id__in=busqueda)
            # Inicio el paginador
            pag = Paginate(request, peliculas, 5)

            # Contexto a retornar a la vista
            cxt = {
                'posts': pag['queryset'],
                'totPost': peliculas,
                'paginator': pag
            }
            url_string = '&'.join(x for x in array_url)
            return render(request, 'busqueda_whoosh.html', {'formulario': formulario, 'peliculas': cxt,'url':url_string, 'datos': datos})

        return render(request, 'busqueda_whoosh.html', {'formulario': formulario, 'peliculas': []})

def crea_indice(request):
    from aplication.busqueda.busquedaWhoosh import crea_indice_peliculas

    crea_indice_peliculas(db_path='.//db.sqlite3',path='aplication//busqueda//indexfilms')

    formulario = PeliculaForm()
    numPeliculas = Pelicula.objects.all().count()
    return render(request, 'principal.html', {'formulario': formulario, 'numPeliculas': numPeliculas})

