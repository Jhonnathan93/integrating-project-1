from django.shortcuts import render
from django.http import JsonResponse
from .methods import *
import os
from .models import Book
import openai
from django.contrib.auth.decorators import login_required

from dotenv import load_dotenv
_ = load_dotenv('keys.env')
openai.api_key  = os.environ['openAI_api_key']

# Create your views here.
def index(request):
    return render(request, 'index.html')


def recomendations(request):
    books = Book.objects.all()
    return render(request, 'recomendations.html', {'books': books})


def response(request):

    if request.method == 'POST':

        detalles = request.POST.get('detalles')
        libro1 = request.POST.get('libro1')
        libro2 = request.POST.get('libro2')
        libro3 = request.POST.get('libro3')

        temas = []
        for tema in ['tema1', 'tema2', 'tema3', 'tema4', 'tema5', 'tema6']:
            if tema in request.POST: temas.append(request.POST[tema])

        genero = []
        for tipo in ['tipo1', 'tipo2', 'tipo3', 'tipo4']:
            if tipo in request.POST: genero.append(request.POST[tipo])
        
        longitud = ''
        if 'longitud' in request.POST: longitud = request.POST.get('longitud')

        prompt = f"Actua como un recomendador de libros y recomiendame libros que sean de {', '.join(temas)} y del tipo {', '.join(genero)} con una longitud aproximada de {longitud} paginas, ademas que sean similares a '{libro1}', '{libro2}' y '{libro3}'. El usuario que pidio estas recomendaciones dejó detalles adicionales para la busqueda: '{detalles}'. dime únicamente los nombres de los libros y su autor, todo en una sola linea, el nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma"
        
        try:

            system_role = 'Eres un bibliotecario, habilidoso dando recomendaciones según lo que te pidan los usuarios. A los usuarios les respondes ÚNICA Y EXCLUSIVAMENTE los nombres de los libros y su autor, todo en una sola linea. El nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma. Por favor no respondas ni des mensaje adicional a lo que se te está pidiendo.'
            user_role = f"Recomiéndame 10 libros o más sobre {', '.join(temas)} y cuyos géneros estén relacionados con {', '.join(genero)}. Me gustan los libros de {longitud} páginas y que están relacionados con {detalles}. Algunos libros que me gustan son '{libro1}', '{libro2}' y '{libro3}'."

            completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": user_role}
                ],
                max_tokens = 900
            )

            libros_recomendados = completion.choices[0].message['content'].replace('"', '').split(';')
            for i in libros_recomendados: print(i)

            info_libros = []
            for libro_recomendado in libros_recomendados:
                libro_info = buscar_libros(libro_recomendado.strip())
                if libro_info: info_libros.append(libro_info)

        except Exception as e:
            # Maneja cualquier error que pueda ocurrir al llamar a la API
            return JsonResponse({'error': str(e)})
        
        # Devuelve la recomendación al usuario
        return render(request, 'response.html', {'respuesta': '', 'libros': info_libros})
    
    else: return render(request, 'index.html')
