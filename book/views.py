from django.shortcuts import render
from django.http import JsonResponse
from .models import Book
from .methods import save_history, buscar_libros
from dotenv import load_dotenv
import os, openai, time
from concurrent.futures import ThreadPoolExecutor
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.models import UserInformation
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User, AnonymousUser
from readinglists.models import ReadingList

def faq(request):
    """
    Renders the Frequently Asked Questions (FAQ) page.

    :param request: Django request object.
    :return: Rendering response for the FAQ page.
    """
    return render(request, 'faq.html')

def index(request):
    """
    Renders the index (homepage) of the application.

    :param request: Django request object.
    :return: Rendering response for the index page.
    """
    return render(request, 'index.html')

def recomendations(request):
    """
    Renders the recommendations page displaying a list of books.

    :param request: Django request object.
    :return: Rendering response for the recommendations page.
    """
    books = Book.objects.all()
    return render(request, 'recomendations.html', {'books': books})

def get_user_info(request):
    """
    Retrieves user information, including disliked books and reading lists.

    :param request: Django request object.
    :return: Tuple containing disliked books and reading list.
    """
    disliked_books = []
    reading_list = None

    if isinstance(request.user, User):
        try:
            user_info = UserInformation.objects.get(user=request.user)
            disliked_books = [book.title for book in user_info.disliked_books.all()]
            reading_list = ReadingList.objects.filter(user=request.user, title="Leer más tarde").first()
        except UserInformation.DoesNotExist:
            user_info = UserInformation.objects.create(user=request.user)
            
        if reading_list is None:
            reading_list = ReadingList.objects.create(user=request.user, title="Leer más tarde")

    return disliked_books, reading_list

def process_books_request(request):
    """
    Processes the book-related information from the request.

    :param request: Django request object.
    :return: Tuple containing details, selected books, topics, genres, and length.
    """
    detalles = request.POST.get('detalles')
    libros = get_selected_items(request.POST, ['libro1', 'libro2', 'libro3', 'libro4'])
    temas = get_selected_items(request.POST, ['Fantasía', 'Romance', 'Historia', 'Suspenso', 'Autoayuda', 'Ciencia Ficción'])
    generos = get_selected_items(request.POST, ['Biografía', 'Novela', 'Científico', 'Poesía'])
    longitud = request.POST.get('longitud', '')

    return detalles, libros, temas, generos, longitud

def get_selected_items(post_data, items):
    """
    Extracts selected items from the POST data.

    :param post_data: POST data from the request.
    :param items: List of items to check for.
    :return: List of selected items.
    """
    return [item for item in items if item in post_data]

def build_openai_messages(user, detalles, libros, temas, generos, longitud, readlater_books_titles, disliked_books):
    """
    Builds messages for OpenAI GPT-3.5 Turbo API.

    :param user: User object.
    :param detalles: Details provided by the user.
    :param libros: Selected books provided by the user.
    :param temas: Selected topics provided by the user.
    :param generos: Selected genres provided by the user.
    :param longitud: Length preference provided by the user.
    :param readlater_books_titles: Titles of books in the user's reading list.
    :param disliked_books: Titles of disliked books.
    :return: Two strings representing system and user messages for OpenAI API.
    """
    msg1 = 'Eres un bibliotecario, habilidoso dando recomendaciones según lo que te pidan los usuarios. Si un usuario te dice que le gusta un libro, NO lo repitas en tus recomendaciones.'
    msg2 = f"Recomiéndame 10 libros o más sobre {', '.join(temas)} y cuyos géneros estén relacionados con {', '.join(generos)}. Me gustan los libros de {longitud} páginas y que están relacionados con {detalles}. Algunos libros que me gustan son {', '.join(libros)}"

    disliked_books_str = ''
    readlater_books_str = ''

    if user:
        if disliked_books:
            disliked_books_str = ', '.join([book.title for book in disliked_books])

        if readlater_books_titles is not None and isinstance(readlater_books_titles, list):
            msg1 += 'Si un usuario te dice que tiene un libro en una lista de "Leer más tarde" vas a tener en cuenta los contenidos del libro para generar tus recomendaciones, pero NO vas a repetir el libro que te dice el usuario.'
            readlater_books_str = f"En mi lista de Leer más tarde, tengo los libros {', '.join(readlater_books_titles)}"

        else:
            readlater_books_str = "No tengo libros en mi lista de Leer más tarde."

        if disliked_books_str:
            msg1 += "Si un usuario te dice que NO le gusta un libro, NO lo vas a recomendar"
            msg2 += f"Ten en cuenta que NO me gustan los siguientes libros {disliked_books_str}"

    msg1 += "A los usuarios les respondes ÚNICA Y EXCLUSIVAMENTE los nombres de los libros en español y su autor, todo en una sola linea. El nombre del libro y el autor separados por un guion y entre libro y libro separado por punto y coma. Por favor no respondas ni des mensaje adicional a lo que se te está pidiendo"

    return msg1, f"{msg2} {readlater_books_str}"

def call_openai_api(msg1, msg2):
    """
    Calls the OpenAI GPT-3.5 Turbo API.

    :param msg1: System message for the API.
    :param msg2: User message for the API.
    :return: List of recommended books.
    """
    start_time = time.time()
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": msg1},
            {"role": "user", "content": msg2}
        ],
        max_tokens=900
    )
    elapsed = time.time() - start_time
    print(f'ChatGPT: {elapsed}s')

    return completion.choices[0].message['content'].replace('"', '').split(';')

def process_google_books_request(libros_recomendados):
    """
    Processes book recommendations using the Google Books API.

    :param libros_recomendados: List of recommended books.
    :return: List of book information retrieved from the Google Books API.
    """
    start_time = time.time()
    info_libros = []

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

    return info_libros

def response(request):
    """
    Handles the recommendation response process.

    :param request: Django request object.
    :return: Rendering response for the recommendation response page.
    """
    if request.method == 'POST':
        disliked_books, reading_list = get_user_info(request)
        detalles, libros, temas, generos, longitud = process_books_request(request)

        _ = load_dotenv('keys.env')
        openai.api_key = os.environ['openAI_api_key']

        msg1, msg2 = build_openai_messages(request.user, detalles, libros, temas, generos, longitud, reading_list, disliked_books)

        libros_recomendados = call_openai_api(msg1, msg2)

        info_libros = process_google_books_request(libros_recomendados)

        save_history(request, _books=', '.join(libros), _topics=', '.join(temas), _genres=', '.join(generos))

        return render(request, 'response.html', {'respuesta': '', 'libros': info_libros})
    else:
        return render(request, 'index.html')  

@login_required
@require_POST
def markAsNotRecommended(request):
    """
    Marks a book as not recommended by the user.

    :param request: Django request object.
    :return: JSON response indicating success or error.
    """
    user_info = UserInformation.objects.get(user=request.user)
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
        
        response_data = {'message': 'No te recomendaremos más este libro'.format()}
        return JsonResponse(response_data)
        
        
    except Exception:
        response_data = {'error': 'An unexpected error occurred'}
        return JsonResponse(response_data, status=500)
