# coding=utf-8

from django.forms import ModelForm
from django import forms

class PeliculaForm(forms.Form):
    Busqueda = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'id': 'search', 'placeholder': 'Título de la pelicula'}))

VALORACIONES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),

)

class PuntuacionForm(forms.Form):
    titulo = forms.CharField(label='Título', required=False)
    sipnosis = forms.CharField(label='Sipnosis', required=False)
    director = forms.CharField(label='Director', required=False)
    actores = forms.CharField(label='Actor', required=False)
    duracion = forms.IntegerField(label='Duración', required=False)
    anyo = forms.IntegerField(label='Año',required=False)
    pais = forms.CharField(label='País',required=False)
    valoracion = forms.ChoiceField(label='Puntuación mayor que',choices=VALORACIONES,required=False)
