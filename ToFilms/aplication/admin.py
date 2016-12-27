from django.contrib import admin
from aplication.models import Director,Actor,Pelicula,Torrent
# Register your models here.

admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Pelicula)
admin.site.register(Torrent)