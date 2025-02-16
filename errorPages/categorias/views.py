from django.shortcuts import render
from django.http import JsonResponse
from .models import Categoria
from .forms import CategoriaForm
from django.shortcuts import redirect

#Metodo que devuelve el JSON
def lista_categorias(request):
    #Obtener todas la instancias del objeto de la BD
    categorias = Categoria.objects.all()

    #Crear una variable en formato de diccionario por que le JSONResponse necesita un diccionario

    data = [
        {
        #Objeto categoria construido al aire
        'nombre': c.nombre,
        'descripcion': c.descripcion,
        'imagen': c.imagen
       }
       for c in categorias
    ]

    #Retornar un JSON
    return JsonResponse(data, safe=False)

    
#Funcion para mandar a la vista del form de categorias
def registrar_categoria(request):

    if request.method == 'POST':
        #Crear una instancia del formulario
        form = CategoriaForm(request.POST)

        #Validar el formulario
        if form.is_valid():
            #Guardar el formulario
            form.save()
            #Redireccionar a la vista de la lista de categorias
            return redirect('registrar')
    else:
        form = CategoriaForm()
    return render(request, 'registrar.html', {'form': form})