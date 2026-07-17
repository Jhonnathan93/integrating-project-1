from django.contrib.auth.models import User
from django.db import transaction

from accounts.models import UserInformation

from .models import Book, History


@transaction.atomic
def history_create(
    *, user: User, books: list[str], topics: list[str], genres: list[str]
) -> History:
    history = History(
        user=user,
        books=", ".join(books),
        topics=", ".join(topics),
        genres=", ".join(genres),
    )
    history.full_clean()
    history.save()
    return history


@transaction.atomic
def disliked_book_add(*, user: User, title: str, author: str) -> Book:
    profile, _ = UserInformation.objects.get_or_create(
        user=user, defaults={"preferences": ""}
    )
    book, _ = Book.objects.get_or_create(title=title, author=author)
    profile.disliked_books.add(book)
    return book
