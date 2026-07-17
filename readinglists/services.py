from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from book.models import Book

from .models import ReadingList

DEFAULT_LIST_TITLE = "Leer más tarde"
MAX_LISTS_PER_USER = 5
MAX_BOOKS_PER_LIST = 15


@transaction.atomic
def reading_list_create_default(*, user: User) -> ReadingList:
    reading_list, _ = ReadingList.objects.get_or_create(
        user=user,
        is_default=True,
        defaults={
            "title": DEFAULT_LIST_TITLE,
            "description": "Tu lista predeterminada",
        },
    )
    return reading_list


@transaction.atomic
def reading_list_create(
    *, user: User, title: str, description: str, cover=None
) -> ReadingList:
    if ReadingList.objects.filter(user=user).count() >= MAX_LISTS_PER_USER:
        raise ValidationError("Excediste la cantidad permitida de listas de lectura.")
    reading_list = ReadingList(
        title=title, description=description, user=user, cover=cover
    )
    reading_list.full_clean()
    reading_list.save()
    return reading_list


@transaction.atomic
def reading_list_update(
    *, reading_list: ReadingList, title: str, description: str, cover=None
) -> ReadingList:
    reading_list.title = title
    reading_list.description = description
    fields = ["title", "description"]
    if cover:
        reading_list.cover = cover
        fields.append("cover")
    reading_list.full_clean()
    reading_list.save(update_fields=fields)
    return reading_list


@transaction.atomic
def book_add_to_reading_list(*, reading_list: ReadingList, book: Book) -> bool:
    if reading_list.books.filter(pk=book.pk).exists():
        return False
    if reading_list.books.count() >= MAX_BOOKS_PER_LIST:
        raise ValidationError("Excediste la cantidad permitida de libros en una lista.")
    reading_list.books.add(book)
    return True
