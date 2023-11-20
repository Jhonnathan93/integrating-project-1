from django.shortcuts import render
from .models import ReadingList
from book.models import Book
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import redirect
from django.conf import settings
import requests
from urllib.parse import quote
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
import os

def overview(request):
    readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'overview.html', {"readinglists": readinglists})

@login_required
@require_POST
def add_to_reading_list(request):
    
    data = json.loads(request.body) 

    title = data.get('title')
    author = data.get('author')
    description = data.get('description')
    buy_link = data.get('buyLink')
    cover= data.get('cover')

    try:
        reading_list = ReadingList.objects.get(user=request.user,title="Leer más tarde")
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
 
    new_book = Book.objects.create(
        title=title,
        author=author,
        description=description,
        buy_link=buy_link,
        cover= cover
    )
    
    if not reading_list.books.filter(id=new_book.id).exists():
        reading_list.books.add(new_book)
        success_message = 'Libro agregado a Leer más tarde'
    else:
        success_message = 'El libro ya está en Leer más tarde'

    data = {'message': success_message}
    return JsonResponse(data)
    
@login_required
def createlist(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        cover = request.FILES.get('cover')
 
        if title and description and cover:
            existing_reading_lists = ReadingList.objects.filter(user=request.user)
            readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')

            if existing_reading_lists.count() >= 4:
                error_message3 = "Excediste la cantidad permitida de reading lists"
                return render(request, 'overview.html', {"readinglists": readinglists, 'error_message': error_message3})

            reading_list = ReadingList(title=title, description=description, cover=cover, user=request.user)
            reading_list.save()
            

            messages.success(request, "Reading list creada exitosamente.")
            return redirect('detail', reading_list.id)

        else:
            messages.error(request, "Error creando la reading list. Verifique la información ingresada.")
            

    else:
        return render(request, 'createlist.html')

def add_book_to_list(request, reading_list, title, author):
    title, author, cover_url, synopsis, average_rating, year, categories, isbn, link = fetch_book_info(title, author)

    if cover_url and synopsis:
        new_book = Book.objects.create(title=title, author=author, cover=cover_url, isbn=isbn)
        reading_list.books.add(new_book)
        new_book.description = synopsis
        dateparts = year.split('-')
        year = int(dateparts[0])
        new_book.year_publication = year
        new_book.topics = categories
        new_book.buy_link = link
        new_book.save()

        messages.success(request, "Libro agregado exitosamente.")
        return True
    else:
        return False

def validate_book_data(title, author):
    return title and author

def detail(request, reading_list_id):
    detail_page = 'detail.html'
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)
    books = reading_list.books.all()

    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')

            if validate_book_data(title, author):
                if reading_list.books.count() <= 14:
                    if not add_book_to_list(request, reading_list, title, author):
                        error_message = "Título o autor inválidos. Verifique la información e inténtelo de nuevo."
                        return render(request, detail_page, {'reading_list': reading_list, 'books': books, 'error_message': error_message})
                else:
                    error_message = "Excediste la cantidad de libros permitida en una reading list"
                    return render(request, detail_page, {'reading_list': reading_list, 'books': books, 'error_message': error_message})
            else:
                error_message = "Título o autor no pueden estar vacíos."
                return render(request, detail_page, {'reading_list': reading_list, 'books': books, 'error_message': error_message})

        print(f"Reading List ID: {reading_list_id}")
        print(f"Number of Books: {books.count()}")

        return render(request, detail_page, {'reading_list': reading_list, 'books': books})

    except ValueError as e:
        print(f"ValueError: {e}")
        error_message = "Ocurrió un error. Verifica los datos de entrada e inténtalo de nuevo."
        return render(request, detail_page, {'reading_list': reading_list, 'books': books, 'error_message': error_message})


"""
def detail(request, reading_list_id):
    detailPage = 'detail.html'
    try:
        reading_list = get_object_or_404(ReadingList, id=reading_list_id)
        books = reading_list.books.all()

        if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')

            if title and author:
                if reading_list.books.count() <= 14:
                    title, author, cover_url, synopsis, average_rating, year, categories, isbn, link = fetch_book_info(title, author)

                    if cover_url and synopsis:
                        new_book = Book.objects.create(title=title, author=author, cover=cover_url, isbn=isbn)
                        reading_list.books.add(new_book)
                        new_book.description = synopsis
                        dateparts = year.split('-')
                        year = int(dateparts[0])
                        new_book.year_publication = year
                        new_book.topics = categories
                        new_book.buy_link = link
                        new_book.save()

                        messages.success(request, "Libro agregado exitosamente.")
                    else:
                        error_message1 = "Título o autor inválidos. Verifique la información e inténtelo de nuevo."
                        return render(request, detailPage, {'reading_list': reading_list, 'books': books, 'error_message': error_message1})
                else:
                    error_message = "Excediste la cantidad de libros permitida en una reading list"
                    return render(request, detailPage, {'reading_list': reading_list, 'books': books, 'error_message': error_message})
            else:
                error_message1 = "Título o autor no pueden estar vacíos."
                return render(request, detailPage, {'reading_list': reading_list, 'books': books, 'error_message': error_message1})
        else:
            books = reading_list.books.all()
            print(f"Reading List ID: {reading_list_id}")
            print(f"Number of Books: {books.count()}")

            if books:
                first_book = books[0]

        return render(request, detailPage, {'reading_list': reading_list, 'books': books})
    except ValueError as e:
        print(f"ValueError: {e}")
        error_message = "Ocurrió un error. Verifica los datos de entrada e inténtalo de nuevo."
        return render(request, detailPage, {'reading_list': reading_list, "books": books, 'error_message': error_message})

"""

def get_google_books_url(encoded_title, encoded_author, order_by, api_key):
    return f'https://www.googleapis.com/books/v1/volumes?q=intitle:{encoded_title}+inauthor:{encoded_author}&orderBy={order_by}&printType=books&langRestrict=es&key={api_key}'

def extract_volume_info(volume_info):
    official_title = volume_info.get('title', 'Title Not Found')
    official_author = ', '.join(volume_info.get('authors', ['Author Not Found']))
    cover_url = volume_info.get('imageLinks', {}).get('thumbnail', None)
    average_rating = volume_info.get('averageRating', 0.0)
    synopsis = volume_info.get('description', '')

    publishing_year = volume_info.get('publishedDate', 'Publication Year Not Found')
    categories = ', '.join(volume_info.get('categories', ['Category Not Found']))
    isbn = volume_info.get('industryIdentifiers', [{'type': 'ISBN_13', 'identifier': 'ISBN no disponible'}])[0]['identifier']
    purchase_link = volume_info.get('infoLink', 'Purchase Link Not Found')

    return {
        'title': official_title,
        'author': official_author,
        'cover_url': cover_url,
        'rating': average_rating,
        'synopsis': synopsis,
        'publishing_year': publishing_year,
        'categories': categories,
        'isbn': isbn,
        'purchase_link': purchase_link
    }

def process_results(items):
    results = []
    for item in items:
        volume_info = item.get('volumeInfo', {})
        result = extract_volume_info(volume_info)
        results.append(result)

    return results

def fetch_book_info(book_title, book_author):
    encoded_title = quote(book_title)
    encoded_author = quote(book_author)
    order_by = 'relevance'
    _ = load_dotenv('keys.env')
    api_key = os.environ.get('googlebooks_api_key')

    while True:
        url = get_google_books_url(encoded_title, encoded_author, order_by, api_key)
        response = requests.get(url)

        print("Fetching book info...")
        print(f"Response Status Code: {response.status_code}")

        try:
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])

            if items:
                results = process_results(items)
                most_relevant_book = next((result for result in results if result['cover_url'] and result['synopsis']), None)

                if most_relevant_book is not None:
                    return most_relevant_book["title"], most_relevant_book["author"], most_relevant_book["cover_url"], most_relevant_book["synopsis"], most_relevant_book["rating"], most_relevant_book["publishing_year"], most_relevant_book["categories"], most_relevant_book["isbn"], most_relevant_book["purchase_link"]
                else:
                    order_by = 'newest'
            else:
                raise ValueError("No books found with the provided title and author.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, None


"""
def fetch_book_info(book_title, book_author):

    encoded_title = quote(book_title)
    encoded_author = quote(book_author)
    
   
    order_by = 'relevance'
    _ = load_dotenv('keys.env')
    api_key  = os.environ['googlebooks_api_key']

    while True:
        
        url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{encoded_title}+inauthor:{encoded_author}&orderBy={order_by}&printType=books&langRestrict=es&key={api_key}'

        response = requests.get(url)
        
        print("Fetching book info...")
        print(f"Response Status Code: {response.status_code}")

        try:
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])

                if items:
                    results = []
                    for item in items:
                        volume_info = item.get('volumeInfo', {})
                        official_title = volume_info.get('title', 'Title Not Found')
                        official_author = ', '.join(volume_info.get('authors', ['Author Not Found']))
                        cover_url = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks'] else None
                        average_rating = volume_info.get('averageRating', 0.0)
                        synopsis = volume_info.get('description', '')

                        publishing_year = volume_info.get('publishedDate', 'Publication Year Not Found')
                        categories = ', '.join(volume_info.get('categories', ['Category Not Found']))
                        isbn = volume_info.get('industryIdentifiers', [{'type': 'ISBN_13', 'identifier': 'ISBN no disponible'}])[0]['identifier']
                        # isbn = ', '.join(volume_info.get('industryIdentifiers', ['ISBN Not Found']))
                        purchase_link = volume_info.get('infoLink', 'Purchase Link Not Found')

                        results.append({
                            'title': official_title,
                            'author': official_author,
                            'cover_url': cover_url,
                            'rating': average_rating,
                            'synopsis': synopsis,

                            'publishing_year': publishing_year,
                            'categories': categories,
                            'isbn': isbn,
                            'purchase_link': purchase_link
                        })

                    
                    most_relevant_book = None
                    for result in results:
                        if result['cover_url'] and result['synopsis']:
                            most_relevant_book = result
                            break
                    
                    if most_relevant_book is not None:
                        
                        return most_relevant_book["title"], most_relevant_book["author"], most_relevant_book["cover_url"], most_relevant_book["synopsis"], most_relevant_book["rating"], most_relevant_book["publishing_year"], most_relevant_book["categories"], most_relevant_book["isbn"], most_relevant_book["purchase_link"]
                    else:
                        
                        order_by = 'newest'
                        
                else:
                    raise ValueError("No books found with the provided title and author.")
            else:
                raise ValueError("Failed to fetch book info from API")

        except ValueError as e:
            print(f"Error: {e}")
            return None, None
"""
@login_required
def updatereadinglist(request, reading_list_id):
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)
    
    if request.method == 'GET':
        
        initial_data = {
            'title': reading_list.title,
            'description': reading_list.description,
            
        }
        
        context = {
            'initial_data': initial_data,
            'reading_list': reading_list,
        }
        return render(request, 'updatereadinglist.html', context)
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        new_cover = request.FILES.get('cover')
        
        if title and description:
           
            reading_list.title = title
            reading_list.description = description
            
            if new_cover:
                reading_list.cover = new_cover
            
            reading_list.save()
            
            return redirect('detail', reading_list.id)
        else:
            return render(request, 'updatereadinglist.html', {'reading_list': reading_list, 'error': 'Bad data in form'})


@login_required
def deletelist(request, reading_list_id):
    reading_list = get_object_or_404(ReadingList, pk=reading_list_id)

    reading_list.delete()
    
    messages.success(request, "Reading list eliminada exitosamente.")
    return redirect('overview') 

@login_required
def deletebook(request, book_id, reading_list_id):
    book = get_object_or_404(Book, pk=book_id) 
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)
    
    book.delete()
    messages.success(request, "Libro eliminado exitosamente.")
    return redirect('detail', reading_list.id)