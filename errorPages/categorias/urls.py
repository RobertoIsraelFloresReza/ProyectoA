from django.urls import path
from .views import *

urlpatterns = [
    path('api/get/', lista_categorias, name='lista'),
    path('registrar/', registrar_categoria, name='registrar'),
]
