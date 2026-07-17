"""Backward-compatible helpers; business operations live in services.py."""

from .google_books import search_book
from .services import history_create


def save_history(request, _books, _topics, _genres):
    return history_create(
        user=request.user,
        books=_books.split(", "),
        topics=_topics.split(", "),
        genres=_genres.split(", "),
    )


def buscar_libros(consulta):
    book = search_book(title=consulta, author="")
    return [book] if book else []
