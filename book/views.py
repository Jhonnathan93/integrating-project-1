from django.shortcuts import render
from django.http import HttpResponse

from .models import Book
from .models import Reader

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

