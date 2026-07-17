from django.contrib.auth.models import User

from accounts.models import UserInformation

from .models import Book


def books_recommended():
    return Book.objects.order_by("-dateAdded")


def disliked_book_titles(*, user: User) -> list[str]:
    return list(
        UserInformation.objects.filter(user=user)
        .values_list("disliked_books__title", flat=True)
    )
