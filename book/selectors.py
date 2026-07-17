from django.contrib.auth.models import User

from .models import Book


def books_recommended():
    return Book.objects.order_by("-dateAdded")


def disliked_book_titles(*, user: User) -> list[str]:
    return list(user.userinformation.disliked_books.values_list("title", flat=True))
