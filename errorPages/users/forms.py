from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                'title': 'La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.',
                'minlength': 8,
                'maxlength': 50,
                'required': True
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirma tu contraseña',
                'title': 'Repite la contraseña',
                'minlength': 8,
                'maxlength': 50,
                'required': True
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel', 
                  'password1', 'password2']
        
        widgets = {
           'email': forms.EmailInput(
                attrs={
                     'class': 'form-control',
                     'pattern': '^[a-zA-Z0-9]+@utez\.edu\.mx$',
                     'placeholder': 'Correo electrónico',
                     'title': 'Mete el correo electrónico institucional ejemplo 20223TN078@utez.edu.mx',
                     'minlength': 5,
                     'maxlength': 50,
                     'required': True
                    }
                
              ),

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'pattern': '^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                    'title': 'Mete tu nombre',
                    'minlength': 2,
                    'maxlength': 50,
                    'required': True
                }
            ),

            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                    'pattern': '^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                    'title': 'Mete tu apellido',
                    'minlength': 2,
                    'maxlength': 50,
                    'required': True
                }
            ),

            'control_number': forms.TextInput(
              attrs={
                  'class': 'form-control',
                  'placeholder': 'Número de control',
                  'pattern': '^\d{5}[A-Z]{2}\d{3}$',
                  'title': 'Formato: 20223TN016 (5 dígitos, 2 letras mayúsculas, 3 dígitos)',
                  'minlength': 10,
                  'maxlength': 10,
                  'required': True
                  }
            ),

            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Edad',
                    'pattern': '[0-9]+',
                    'title': 'Mete tu edad',
                    'min': 18,
                    'max': 100,
                    'required': True
                }
            ),

            'tel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Teléfono',
                    'pattern': '[0-9]+',
                    'title': 'Mete tu número de teléfono',
                    'minlength': 10,
                    'maxlength': 10,
                    'required': True
                }
            ),
        }



class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico', max_length=150)  # Cambia 'email' por 'username'
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')  # Aquí sigue llamándose username
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Usuario o contraseña incorrectos')
        return cleaned_data

    pass



def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@utez.edu.mx'):
            raise forms.ValidationError('El correo debe ser institucional de la UTEZ (ejemplo: 20223TN078@utez.edu.mx)')
        if len(email) < 5 or len(email) > 50:
            raise forms.ValidationError('El correo debe tener entre 5 y 50 caracteres.')
        return email

def clean_control_number(self):
        control_number = self.cleaned_data.get('control_number')
        if len(control_number) != 10:
            raise forms.ValidationError('El número de control debe tener exactamente 10 caracteres.')
        if not control_number[:5].isdigit() or not control_number[5:7].isalpha() or not control_number[7:].isdigit():
            raise forms.ValidationError('El número de control debe seguir el formato: 20223TN016')
        return control_number

def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if len(tel) != 10 or not tel.isdigit():
            raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        return tel

def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Validación de contraseñas
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        # Validación del formato de la contraseña
        if len(password1) < 8 or len(password1) > 50:
            raise forms.ValidationError('La contraseña debe tener entre 8 y 50 caracteres.')
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password1):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula, una minúscula, un número y un carácter especial.')
        
        return cleaned_data