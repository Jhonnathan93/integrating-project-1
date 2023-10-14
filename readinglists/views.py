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



def overview(request):
    readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'overview.html', {"readinglists": readinglists})

@login_required
def createlist(request):

    if request.method == 'POST':
        form = ReadingListForm(request.POST, request.FILES)
        books = []
        print(request.POST)
 
        if form.is_valid():
            existing_reading_lists = ReadingList.objects.filter(user=request.user)
            readinglists = ReadingList.objects.filter(user=request.user).order_by('-date_created')

            if existing_reading_lists.count() >= 3:
                error_message3 = "Excediste la cantidad permitida de reading lists"
                return render(request, 'overview.html', {"readinglists": readinglists, 'error_message': error_message3})

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
    print("Inside detail view...")
    try:
        reading_list = get_object_or_404(ReadingList, id=reading_list_id)
        books = reading_list.books.all()
        
        if request.method == 'POST':
            book_form = AddBookForm(request.POST)
            if book_form.is_valid():
                
                if reading_list.books.count() <= 14:
                    
                
                    title_form = book_form.cleaned_data['title']
                    author_form = book_form.cleaned_data['author']
                    
                    title, author,cover_url, synopsis, average_rating = fetch_book_info(title_form, author_form)
                    
                    if cover_url and synopsis:
                        
                        new_book = Book.objects.create(title=title, author=author)
                        reading_list.books.add(new_book)
                        new_book.cover = cover_url
                        
                        new_book.description = synopsis
                        new_book.save()
                        messages.success(request, "Libro agregado exitosamente.")
                    else: 
                        error_message1 = "Título o autor inválidos. Verifique la información e inténtelo de nuevo."
                        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message1})
                    
                else:
                    
                    return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message2})
                    
            else:
                
                return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books})
        else:
            
            book_form = AddBookForm()

        books = reading_list.books.all()

        print(f"Reading List ID: {reading_list_id}")
        print(f"Number of Books: {books.count()}")

        if books:
            first_book = books[0]
            print(f"First Book Title: {first_book.title}")
            print(f"First Book Author: {first_book.author}")
        
        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books})

    except ValueError as e:
        print(f"ValueError: {e}")
        error_message = "An error occurred. Please check your input and try again."
        return render(request, 'detail.html', {'reading_list': reading_list, 'book_form': book_form, "books": books, 'error_message': error_message})


def fetch_book_info(book_title, book_author):
    api_key = ""
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}+inauthor:{book_author}&orderBy=relevance&printType=books&key={api_key}'

    response = requests.get(url)

    print("Fetching book info...")
    print(f"Response Status Code: {response.status_code}")

    try:
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                volume_info = items[0].get('volumeInfo', {})
                official_title = volume_info.get('title', 'Title Not Found')
                official_author = ', '.join(volume_info.get('authors', ['Author Not Found']))
                cover_url = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks'] else None
                average_rating = volume_info.get('averageRating', 0.0)
                synopsis = volume_info.get('description', '')
                
                if cover_url and cover_url.startswith('http'):
                    
                    return official_title, official_author, cover_url, synopsis, average_rating
                else:
                    raise ValueError("No cover URL available for this book.")
            else:
                raise ValueError("No book found with the provided title and author.")
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
    book = get_object_or_404(Book, pk=book_id)  # Replace 'Book' with your actual model name
    reading_list = get_object_or_404(ReadingList, id=reading_list_id)
    
    book.delete()
    messages.success(request, "Libro eliminado exitosamente.")
    return redirect('detail', reading_list.id)  # Redirect to the reading list detail page
