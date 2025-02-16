from .models import Producto
from django import forms

##Crear una clase para cada formulario que necesitemos

class ProductoForm(forms.ModelForm):
    #Definir los metadatos de la clase
    class Meta:
        #Definir el modelo al que pertenece el formulario
        model = Producto
        #Definir los campos del modelo que se van a mostrar en el formulario
        fields = ['nombre', 'precio', 'imagen']
        #Definir los atributos de los campos del formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.URLInput(attrs={'class': 'form-control'})
        }

        #Personalizar las etiquetas o los textos que salen a lado de los inputs del formulario

        labels = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio (MXN)',
            'imagen': 'URL de la imagen del producto'
        }

        #Personalizar los mensajes de error de los campos del formulario

        error_messages = {
            'nombre': {
                'required': 'El nombre del producto es obligatorio',
                'unique': 'El nombre del producto ya existe'
            },
            'precio': {
                'required': 'El precio del producto es obligatorio',
                'invalid': 'El precio del producto debe ser un número'
            },
            'imagen': {
                'required': 'La URL de la imagen del producto es obligatoria',
                'invalid': 'La URL de la imagen del producto debe ser válida'
            }
        }

