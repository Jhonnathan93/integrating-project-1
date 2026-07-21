from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from accounts.models import UserInformation
from book.models import Book
from book.selectors import books_recommended, disliked_book_titles


class BookSelectorsTests(TestCase):
    def test_books_recommended_orders_books_by_most_recent(self) -> None:
        older = Book.objects.create(title="Older", author="Author")
        newer = Book.objects.create(title="Newer", author="Author")
        Book.objects.filter(pk=older.pk).update(
            dateAdded=timezone.now() - timedelta(days=1)
        )

        self.assertEqual(list(books_recommended()), [newer, older])

    def test_disliked_book_titles_returns_only_titles_for_the_requested_user(
        self,
    ) -> None:
        user = User.objects.create_user(username="reader", password="password")
        another_user = User.objects.create_user(username="another", password="password")
        disliked = Book.objects.create(title="Dune", author="Frank Herbert")
        other_disliked = Book.objects.create(title="Other", author="Author")
        profile = UserInformation.objects.create(user=user, preferences="")
        another_profile = UserInformation.objects.create(
            user=another_user, preferences=""
        )
        profile.disliked_books.add(disliked)
        another_profile.disliked_books.add(other_disliked)

        self.assertEqual(disliked_book_titles(user=user), ["Dune"])
