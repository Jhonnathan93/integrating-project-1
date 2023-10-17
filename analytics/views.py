from django.shortcuts import render
from django.db.models import Count
from book.models import Book
from django.db.models import F
from django.db.models import Subquery

# Create your views here.
def top_books(request):
    top_books = Book.objects.values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('-book_count')[:5]

    least_books = Book.objects.values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('book_count')[:5]

    print(top_books)
    return render(request, 'top_books.html', {'top_books': top_books, 'least_books': least_books})