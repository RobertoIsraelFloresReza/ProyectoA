from .models import Categoria
from django import forms


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria

        fields = ['nombre', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la categoría'}),
            'imagen': forms.URLInput(attrs={'class': 'form-control'})
        }


        labels = {
            'nombre': 'Nombre de la categoría',
            'descripcion': 'Descripción de la categoría',
            'imagen': 'URL de la imagen de la categoría'
        }

        error_messages = {
            'nombre': {
                'required': 'El nombre de la categoría es obligatorio',
                'unique': 'El nombre de la categoría ya existe'
            },
            'descripcion': {
                'required': 'La descripción de la categoría es obligatoria'
            },
            'imagen': {
                'required': 'La URL de la imagen de la categoría es obligatoria',
                'invalid': 'La URL de la imagen de la categoría debe ser válida'
            }
        }

        