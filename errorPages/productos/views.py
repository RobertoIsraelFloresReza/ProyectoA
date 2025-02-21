import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

#Metodo que devuelve el JSON
def lista_productos(request):
    #Obtener todas la instancias del objeto de la BD
    productos = Producto.objects.all()

    #Crear una variable en formato de diccionario por que le JSONResponse necesita un diccionario

    data = [
        {
        #Objeto producto construido al aire
        'id': p.id,
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


#Funcion que registre sin recaragar la pagina osea sin hacer render 
def registrar_producto(request):
    #chacar que estemos manejando un metodo POST
    if request.method == 'POST':
        #aqui se puede validar si hay sesion antes de hacer el registro
        try :
            #intentar obtener los datos del body request 
            data = json.loads(request.body)# hace que el parametro que se recibe se convierta en un json
            #Crear una instancia del modelo 
            producto = Producto.objects.create(
                #basicamente es un constructor de objetos
                nombre = data['nombre'],
                precio = data['precio'],
                imagen = data['imagen']
            )#la funcion create directamente guarda el objeto en la BD
            #Retornar un JSON
            return JsonResponse({'mensaje': 'Registro exitoso', 'id':producto.id}, status=201)
        except Exception as e:
            #Retornar un JSON con un mensaje de error
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)


#El metodo de api PUT PUT = ACTUALIZAR
def actualizar_producto(request, id_producto):
    #
    if request.method == 'PUT':
        #Intentar actualizar el objeto
        #1) Obtener la entidad a actualizar
        #Parametros: modelo y id o identificador del objeto
        producto = get_object_or_404(Producto, id=id_producto)

        try:
            #2) Obtener los datos del body request
            data = json.loads(request.body)
            #3) Actualizar cada campo disponible de la entidad 
            producto.nombre = data.get('nombre', producto.nombre)
            producto.precio = data.get('precio', producto.precio)
            producto.imagen = data.get('imagen', producto.imagen)
            #4) Guardar los cambios
            producto.save()
            #5)Retornar un JSON
            return JsonResponse({'mensaje': 'Actualizacion exitosa'}, status=200)
        except Exception as e:
            #Retornar un JSON con un mensaje de error
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)



#El metodo de api DELETE DELETE = ELIMINAR

def borrar_producto(request, id_producto):
    #Validar que el metodo sea DELETE
    if request.method == 'DELETE':
        #Intentar eliminar el objeto
        #1) Obtener la entidad a eliminar
        #Parametros: modelo y id o identificador del objeto
        producto = get_object_or_404(Producto, id=id_producto)
        try:
            #2) Eliminar la entidad
            producto.delete() #<-- la funcion delete elimina el objeto de la BD
            #3) Retornar un JSON
            return JsonResponse({'mensaje': 'Eliminacion exitosa'}, status=200)
        except Exception as e:
            #Retornar un JSON con un mensaje de error
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)


# Crear un metodo que devuelva solo un objeto de la BD 
def obtener_producto(request, id_producto):
    
    if request.method == 'GET':
        #Intentar obtener el objeto
        #1) Obtener la entidad a obtener
        #Parametros: modelo y id o identificador del objeto
        producto = get_object_or_404(Producto, id=id_producto)
        try:
            #2) Crear un diccionario con los datos del objeto
            data = {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'imagen': producto.imagen
            }
            #3) Retornar un JSON
            return JsonResponse(data, status=200)
        except Exception as e:
            #Retornar un JSON con un mensaje de error
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)
