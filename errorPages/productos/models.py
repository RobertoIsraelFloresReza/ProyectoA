from django.db import models

class Producto(models.Model):
    #Atributos de la clase
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()


    def __str__(self):
        return self.nombre


    