from django.shortcuts import render
from django.db.models import Count
from book.models import Book
from django.db.models import F
from django.db.models import Subquery
from datetime import datetime, timedelta


def top_books(request, period="all"):
    end_date = datetime.now()
    start_date = None
    
    if period == "week":
        start_date = end_date - timedelta(weeks=1)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "6months":
        start_date = end_date - timedelta(days=180)
    elif period == "year":
        start_date = end_date - timedelta(days=365)
    
    if start_date:
        top_books = Book.objects.filter(dateAdded__range=(start_date, end_date)).values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('-book_count')[:5]
        least_books = Book.objects.filter(dateAdded__range=(start_date, end_date)).values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('book_count')[:5]
    else:
        top_books = Book.objects.values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('-book_count')[:5]
        least_books = Book.objects.values('title', 'isbn').annotate(book_count=Count('isbn')).order_by('book_count')[:5]
    
    return render(request, 'top_books.html', {'top_books': top_books, 'least_books': least_books, 'period': period})
