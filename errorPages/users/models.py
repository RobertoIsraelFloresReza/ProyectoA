from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    control_number = models.CharField(max_length=20, unique=True)
    age = models.PositiveIntegerField()
    tel = models.CharField(max_length=10)
    join_date = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'control_number', 'age', 'tel']
    
    def __str__(self):
        return self.email


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