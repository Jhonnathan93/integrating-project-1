from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from analytics.selectors import book_rankings
from book.models import Book


class BookRankingsTests(TestCase):
    def test_book_rankings_filters_books_by_requested_period(self) -> None:
        recent = Book.objects.create(title="Recent", author="Author", isbn="recent")
        older = Book.objects.create(title="Older", author="Author", isbn="older")
        Book.objects.filter(pk=older.pk).update(
            dateAdded=timezone.now() - timedelta(days=10)
        )

        top_books, least_books = book_rankings(period="week")

        self.assertEqual(
            list(top_books),
            [{"title": recent.title, "isbn": recent.isbn, "book_count": 1}],
        )
        self.assertEqual(
            list(least_books),
            [{"title": recent.title, "isbn": recent.isbn, "book_count": 1}],
        )
