from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserInformation
from book.services import disliked_book_add


class DislikedBookAddTests(TestCase):
    def test_disliked_book_add_creates_profile_and_links_book_once(self) -> None:
        user = User.objects.create_user(username="reader", password="password")

        first_book = disliked_book_add(user=user, title="Dune", author="Frank Herbert")
        second_book = disliked_book_add(user=user, title="Dune", author="Frank Herbert")

        profile = UserInformation.objects.get(user=user)
        self.assertEqual(first_book, second_book)
        self.assertEqual(profile.disliked_books.count(), 1)
