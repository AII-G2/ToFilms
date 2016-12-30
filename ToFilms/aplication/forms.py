# coding=utf-8

from django.forms import ModelForm
from django import forms

class PeliculaForm(forms.Form):
    Busqueda = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={'id': 'search', 'placeholder': 'Título de la pelicula'}))


