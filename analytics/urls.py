from django.urls import path

from . import views

urlpatterns = [
    path("", views.top_books, name="top_books"),
    path("<str:period>/", views.top_books, name="top_books_period"),
]
