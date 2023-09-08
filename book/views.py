from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Book
import os
import openai
from .models import Book
from .models import Reader

api_key = "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"

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')


def recomendations(request):
    books = Book.objects.all()
    return render(request, 'recomendations.html', {'books': books})

def profile(request):
    books = Book.objects.all()
    reader = Reader.objects.first()
    return render(request, 'profile.html', {'books': books, 'reader': reader})

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
        prompt = f"Recomienda libros que son {', '.join(temas)} y del tipo {', '.join(tipos_libro)} con longitud {longitud}. También me gustaría libros similares a '{libro1}', '{libro2}' y '{libro3}'."
        
        # Llama a la API de ChatGPT para obtener recomendaciones
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",  # Puedes ajustar el motor según tus necesidades
                prompt=prompt,
                max_tokens=50, # Ajusta la cantidad de tokens según tu necesidad
                api_key=api_key
            )
            recomendaciones = response.choices[0].text.strip()
        except Exception as e:
            # Maneja cualquier error que pueda ocurrir al llamar a la API
            return JsonResponse({'error': str(e)})
        
        # Devuelve la recomendación al usuario
        return render(request, 'response.html', {'respuesta': recomendaciones})
    
    else:
        # Si la solicitud no es POST, puedes manejarla de acuerdo a tus necesidades
        # Por ejemplo, mostrar el formulario vacío
        return render(request, 'index.html')