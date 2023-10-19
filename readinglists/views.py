from django.shortcuts import render
from .models import ReadingList
from book.models import Book
from .forms import ReadingListForm
from .forms import AddBookForm
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import redirect
from django.conf import settings
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import os
from django.http import JsonResponse

_ = load_dotenv('keys.env')
api_key  = os.environ['googlebooks_api_key']

def overview(request):
    readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'overview.html', {"readinglists": readinglists})

@login_required
def createlist(request):

    existing_reading_lists = ReadingList.objects.filter(user=request.user)
    if request.method == 'POST':
        
        if existing_reading_lists.count() >= 4:
            error_message3 = "Excediste la cantidad permitida de reading lists"
            return render(request, 'overview.html', {"readinglists": readinglists, 'error_message': error_message3})
        else:
            form = ReadingListForm(request.POST, request.FILES)
            books = []
 
        if form.is_valid():
            readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')

            reading_list = form.save(commit=False)
            reading_list.user = request.user
            reading_list.save()

            messages.success(request, "Reading list creada exitosamente.")
            return redirect('detail', reading_list.id)

        else:
            messages.error(request, "Error creando la reading list. Verifique la información ingresada.")
            print(form.errors)

    else:
        form = ReadingListForm()

    return render(request, 'createlist.html', {'form': form})

def detail(request, reading_list_id):
    
    try:
        reading_list = get_object_or_404(ReadingList, id=reading_list_id)
        books = reading_list.books.all()
        
        if request.method == 'POST':
            book_form = AddBookForm(request.POST)
            if book_form.is_valid():
                
                if reading_list.books.count() <= 14:
                    
                    title_form = book_form.cleaned_data['title']
                    author_form = book_form.cleaned_data['author']
                    
                    title, author,cover_url, synopsis, average_rating, year, categories, isbn, link = fetch_book_info(title_form, author_form)
                    
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
                        print("holaaa")
                        print(new_book.cover)
                        messages.success(request, "Libro agregado exitosamente.")
                    else: 
                        error_message1 = "Título o autor inválidos. Verifique la información e inténtelo de nuevo."
                        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message1})
                    
                else:
                    error_message = "Exediste la cantidad de libros permitida en una reading list"
                    return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message})
                    
            else:
                return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books})
        else:
            book_form = AddBookForm()

        books = reading_list.books.all()

        if books:
            first_book = books[0]

            print(books[0].cover)
        
        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books})

    except ValueError as e:
        print(f"ValueError: {e}")
        error_message = "Ocurrió un error. Verifica los datos de entrada e inténtalo de nuevo."
        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message})



def fetch_book_info(book_title, book_author):

    encoded_title = quote(book_title)
    encoded_author = quote(book_author)
    order_by = 'relevance'

    while True:
        
        url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{encoded_title}+inauthor:{encoded_author}&orderBy={order_by}&printType=books&langRestrict=es&key={api_key}'

        response = requests.get(url)


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
                        synopsis = volume_info.get('description', 'Sin descripción disponible')

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

@login_required
def updatereadinglist(request, reading_list_id):
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)
    if request.method == 'GET':
        form1 = ReadingListForm(instance=reading_list)
        context = {
        'form': form1,
        'reading_list': reading_list,
    }
        return render(request, 'updatereadinglist.html', context)
    else:
        try:
            form = ReadingListForm(request.POST, request.FILES, instance=reading_list)
            new_cover = request.FILES.get('cover')
            if new_cover:
                reading_list.cover = new_cover
            form.save()
            return redirect('detail', reading_list.id)
        except ValueError:
            return render(request, 'updatereadinglist.html',{'reading_list': reading_list,'form':form,'error':'Bad data in form'})
        
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