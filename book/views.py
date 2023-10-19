from django.shortcuts import render
from django.http import JsonResponse
from .models import Book
from .methods import *
from dotenv import load_dotenv
import os, openai

def index(request):
    return render(request, 'index.html')


def recomendations(request):
    books = Book.objects.all()
    return render(request, 'recomendations.html', {'books': books})


def response(request):

    if request.method == 'POST':

        detalles = request.POST.get('detalles')

        libros = []
        for libro in ['libro1', 'libro2', 'libro3']:
            if libro in request.POST: libros.append(request.POST[libro])

        temas = []
        for tema in ['Fantasía', 'Romance', 'Historia', 'Suspenso', 'Autoayuda', 'Ciencia Ficción']:
            if tema in request.POST: temas.append(request.POST[tema])

        generos = []
        for tipo in ['Biografía', 'Novela', 'Científico', 'Poesía']:
            if tipo in request.POST: generos.append(request.POST[tipo])
        
        longitud = ''
        if 'longitud' in request.POST: longitud = request.POST.get('longitud')

        print('antes de asignar la api')
        
        _ = load_dotenv('keys.env')
        openai.api_key  = os.environ['openAI_api_key']

        try:
            completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content":  'Eres un bibliotecario, habilidoso dando recomendaciones según lo que te pidan los usuarios, y los libros que te piden los usuarios no los vas a repetir en tus recomendaciones. A los usuarios les respondes ÚNICA Y EXCLUSIVAMENTE los nombres de los libros en español y su autor, todo en una sola linea. El nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma. Por favor no respondas ni des mensaje adicional a lo que se te está pidiendo.'},
                    {"role": "user", "content": f"Recomiéndame 10 libros o más sobre {', '.join(temas)} y cuyos géneros estén relacionados con {', '.join(generos)}. Me gustan los libros de {longitud} páginas y que están relacionados con {detalles}. Algunos libros que me gustan son {', '.join(libros)}"}
                ],
                max_tokens = 900
            )

            libros_recomendados = completion.choices[0].message['content'].replace('"', '').split(';')
            info_libros = []
            for libro_recomendado in libros_recomendados:
                libro_info = buscar_libros(libro_recomendado.strip())
                if libro_info: info_libros.append(libro_info)

        except Exception as e: return JsonResponse({'error': str(e)})

        print("antes de save_history")
        save_history(request, _books=', '.join(libros), _topics=', '.join(temas), _genres=', '.join(generos))
        print("después de save_history")
        
        return render(request, 'response.html', {'respuesta': '', 'libros': info_libros})
    
    else: return render(request, 'index.html')