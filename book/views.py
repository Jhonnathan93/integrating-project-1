from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Book
import os
import openai
from .models import Book
from .models import Reader
from .methods import *
from django.contrib.auth.decorators import login_required


api_key = "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"

# Create your views here.
def index(request):
    return render(request, 'index.html')


def recomendations(request):
    books = Book.objects.all()
    return render(request, 'recomendations.html', {'books': books})

@login_required  # Asegura que el usuario esté autenticado
def profile(request):
    user = request.user  # Obtén el usuario actualmente autenticado
    print(user)
    return render(request, 'profile.html', {'user': user})

def response(request):
    if request.method == 'POST':
        print("Valor de la clave API:", api_key)
        # Obtén los datos del formulario
        libro1 = request.POST.get('libro1')
        libro2 = request.POST.get('libro2')
        libro3 = request.POST.get('libro3')
        
        # Obtén los temas seleccionados
        temas = []
        if 'tema1' in request.POST:
            temas.append(request.POST['tema1'])
        if 'tema2' in request.POST:
            temas.append(request.POST['tema2'])
        if 'tema3' in request.POST:
            temas.append(request.POST['tema3'])
        
        # Obtén los tipos de libro seleccionados
        tipos_libro = []
        if 'tipo1' in request.POST:
            tipos_libro.append(request.POST['tipo1'])
        if 'tipo2' in request.POST:
            tipos_libro.append(request.POST['tipo2'])
        if 'tipo3' in request.POST:
            tipos_libro.append(request.POST['tipo3'])
        
        # Obtén la longitud seleccionada
        longitud = None
        if 'longitud1' in request.POST:
            longitud = 'corto'
        elif 'longitud2' in request.POST:
            longitud = 'medio'
        elif 'longitud3' in request.POST:
            longitud = 'largo'

        # Crea un prompt basado en las selecciones del usuario
        prompt = f"Actua como un recomendador de libros y recomiendame libros que sean de {', '.join(temas)} y del tipo {', '.join(tipos_libro)} con longitud {longitud}, ademas que sean similares a '{libro1}', '{libro2}' y '{libro3}'. dime unicamente los nombres de los libros y su autor, todo en una sola linea, el nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma"
        
        # Llama a la API de ChatGPT para obtener recomendaciones
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",  # Puedes ajustar el motor según tus necesidades
                prompt=prompt,
                max_tokens=65, # Ajusta la cantidad de tokens según tu necesidad
                api_key=api_key
            )
            recomendaciones = response.choices[0].text.strip()

            # Divide las recomendaciones por punto y coma para obtener los nombres de los libros
            libros_recomendados = recomendaciones.split(';')
            print(libros_recomendados)
            # Inicializa una lista para almacenar la información detallada de los libros
            info_libros = []

            # Búsqueda de información detallada para cada libro recomendado
            for libro_recomendado in libros_recomendados:
                libro_info = buscar_libros(libro_recomendado.strip(), max_resultados=1)
                if libro_info:
                    info_libros.append(libro_info)

        except Exception as e:
            # Maneja cualquier error que pueda ocurrir al llamar a la API
            return JsonResponse({'error': str(e)})
        
        # Devuelve la recomendación al usuario
        return render(request, 'response.html', {'respuesta': recomendaciones, 'libros': info_libros})
    
    else:
        # Si la solicitud no es POST, puedes manejarla de acuerdo a tus necesidades
        # Por ejemplo, mostrar el formulario vacío
        return render(request, 'index.html')