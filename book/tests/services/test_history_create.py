from django.contrib.auth.models import User
from django.test import TestCase

from book.services import history_create


class HistoryCreateTests(TestCase):
    def test_history_create_persists_selected_books_topics_and_genres(self) -> None:
        user = User.objects.create_user(username="reader", password="password")

        history = history_create(
            user=user,
            books=["Dune", "Foundation"],
            topics=["Fantasy", "Space"],
            genres=["Novel"],
        )

        self.assertEqual(history.books, "Dune, Foundation")
        self.assertEqual(history.topics, "Fantasy, Space")
        self.assertEqual(history.genres, "Novel")
