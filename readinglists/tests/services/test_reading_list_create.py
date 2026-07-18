from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from book.models import Book
from readinglists.models import ReadingList
from readinglists.services import (
    MAX_LISTS_PER_USER,
    book_add_to_reading_list,
    reading_list_create,
    reading_list_create_default,
)


class ReadingListCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="reader", password="password")

    def test_default_reading_list_is_idempotent(self) -> None:
        first_list = reading_list_create_default(user=self.user)
        second_list = reading_list_create_default(user=self.user)

        self.assertEqual(first_list, second_list)
        self.assertEqual(ReadingList.objects.filter(user=self.user, is_default=True).count(), 1)

    def test_reading_list_create_enforces_user_limit(self) -> None:
        for index in range(MAX_LISTS_PER_USER):
            ReadingList.objects.create(
                user=self.user,
                title=f"List {index}",
                description="Description",
            )

        with self.assertRaises(ValidationError):
            reading_list_create(
                user=self.user,
                title="Overflow",
                description="Description",
            )

    def test_book_add_to_reading_list_prevents_duplicates(self) -> None:
        reading_list = reading_list_create(
            user=self.user,
            title="Favorites",
            description="Description",
        )
        book = Book.objects.create(title="Dune", author="Frank Herbert")

        self.assertTrue(book_add_to_reading_list(reading_list=reading_list, book=book))
        self.assertFalse(book_add_to_reading_list(reading_list=reading_list, book=book))
        self.assertEqual(reading_list.books.count(), 1)
