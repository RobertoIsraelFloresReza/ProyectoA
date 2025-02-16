from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from django.shortcuts import redirect

#Metodo que devuelve el JSON
def lista_productos(request):
    #Obtener todas la instancias del objeto de la BD
    productos = Producto.objects.all()

    #Crear una variable en formato de diccionario por que le JSONResponse necesita un diccionario

    data = [
        {
        #Objeto producto construido al aire
        'nombre': p.nombre,
        'precio': p.precio,
        'imagen': p.imagen
       }
       for p in productos
    ]

    #Retornar un JSON
    return JsonResponse(data, safe=False)

#Funcion para mandar a la vista del form de productos
def agregar_producto(request):

    if request.method == 'POST':
        #Crear una instancia del formulario
        form = ProductoForm(request.POST)

        #Validar el formulario
        if form.is_valid():
            #Guardar el formulario
            form.save()
            #Redireccionar a la vista de la lista de productos
            return redirect('agregar')
    else:
        form = ProductoForm()
    return render(request, 'agregar.html', {'form': form})



