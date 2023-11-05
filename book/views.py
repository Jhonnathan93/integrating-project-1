from django.shortcuts import render
from django.http import JsonResponse
from .models import Book
from .methods import *
from dotenv import load_dotenv
import os, openai, time
from concurrent.futures import ThreadPoolExecutor
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.models import userInformation
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, AnonymousUser
from readinglists.models import ReadingList


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
        

        _ = load_dotenv('keys.env')
        openai.api_key  = os.environ['openAI_api_key']
        
        msg1 = 'Eres un bibliotecario, habilidoso dando recomendaciones según lo que te pidan los usuarios. Si un usuario te dice que le gusta un libro, NO lo repitas en tus recomendaciones.'
        msg2 = f"Recomiéndame 10 libros o más sobre {', '.join(temas)} y cuyos géneros estén relacionados con {', '.join(generos)}. Me gustan los libros de {longitud} páginas y que están relacionados con {detalles}. Algunos libros que me gustan son {', '.join(libros)}" 
            
        
        if isinstance(request.user, User):
            user_info = userInformation.objects.get(user=request.user)
            
            disliked_books = [book.title for book in user_info.disliked_books.all()]
            reading_list = ReadingList.objects.filter(user=request.user, title="Leer más tarde").first()
            readlater_books = reading_list.books.all()
            readlater_books_titles = [book.title for book in readlater_books]
            
            
            if readlater_books:
                
                readlater_books_str = ', '.join(readlater_books_titles)
                print(f"read later books: {readlater_books_str}")
                msg1 += 'Si un usuario te dice que tiene un libro en una lista de "Leer más tarde" vas a tener en cuenta los contenidos del libro para generar tus recomendaciones, pero NO vas a repetir el libro que te dice el usuario.'
                msg2 += f"En mi lista de Leer más tarde, tengo los libros {readlater_books_str}"
                
            if disliked_books:
                
                disliked_books_str = ', '.join(disliked_books)
                
                print(f"disliked books: {disliked_books_str}")
                
                msg1 +=  f"Si un usuario te dice que NO le gusta un libro, NO lo vas a recomendar"
                msg2 += f"Ten en cuenta que NO me gustan los siguientes libros {disliked_books_str}"

                
            
        msg1 += "A los usuarios les respondes ÚNICA Y EXCLUSIVAMENTE los nombres de los libros en español y su autor, todo en una sola linea. El nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma. Por favor no respondas ni des mensaje adicional a lo que se te está pidiendo"        
                       
        start_time = time.time()
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content":  msg1},
                {"role": "user", "content": msg2}
            ],
            max_tokens = 900
        )
        elapsed = time.time() - start_time
        print(f'ChatGPT: {elapsed}s')

        libros_recomendados = completion.choices[0].message['content'].replace('"', '').split(';')
        info_libros = []

        start_time = time.time()
        
        try:
            
            executor = ThreadPoolExecutor(len(libros_recomendados))
            
            futures = []
            
            print("libros chatgpt:")
            for libro_recomendado in libros_recomendados:
                
                print(libro_recomendado)
                future = executor.submit(buscar_libros, (libro_recomendado.strip()))
                futures.append(future)

            for future in futures:
                info_libros.append(future.result())


        except Exception as e:
            return JsonResponse({'error': str(e)})
        
        elapsed = time.time() - start_time
        print(f'Google Books: {elapsed}s')

        save_history(request, _books=', '.join(libros), _topics=', '.join(temas), _genres=', '.join(generos))
        
        return render(request, 'response.html', {'respuesta': '', 'libros': info_libros})
    
    else: return render(request, 'index.html')
    
@login_required
@require_POST
def markasNotRecommended(request):
    
    user_info = userInformation.objects.get(user=request.user)
    data = json.loads(request.body) 
    
    title = data.get('title')
    author = data.get('author')
    
    try:
        
        disliked_book = Book.objects.create(
        title=title,
        author=author,
        )
        
        user_info.disliked_books.add(disliked_book)
        user_info.save()
        
        disliked_book.disliked_by.add(user_info)
        disliked_book.save()
        
        response_data = {'message': f'No te recomendaremos más este libro'}
        return JsonResponse(response_data)
        
        
    except Exception as e:
        response_data = {'error': 'An unexpected error occurred'}
        return JsonResponse(response_data, status=500)