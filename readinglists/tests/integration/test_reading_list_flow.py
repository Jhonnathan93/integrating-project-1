from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from readinglists.models import ReadingList


@tag("integration")
class ReadingListFlowIntegrationTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="reader", password="secure-password"
        )
        self.client.force_login(self.user)

    @patch("readinglists.views.search_book")
    def test_create_list_add_book_and_remove_book(self, search_book: Mock) -> None:
        create_response = self.client.post(
            reverse("createlist"),
            {"title": "Favorites", "description": "Books to revisit"},
        )
        reading_list = ReadingList.objects.get(user=self.user, title="Favorites")
        search_book.return_value = {
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "A science-fiction novel.",
            "cover": "https://example.com/dune.jpg",
            "buy_link": "https://example.com/dune",
        }

        add_response = self.client.post(
            reverse("detail", args=[reading_list.pk]),
            {"title": "Dune", "author": "Frank Herbert"},
        )
        book = reading_list.books.get(title="Dune")
        remove_response = self.client.post(
            reverse("deletebook", args=[reading_list.pk, book.pk])
        )

        self.assertRedirects(create_response, reverse("detail", args=[reading_list.pk]))
        self.assertRedirects(add_response, reverse("detail", args=[reading_list.pk]))
        self.assertRedirects(remove_response, reverse("detail", args=[reading_list.pk]))
        self.assertFalse(reading_list.books.filter(pk=book.pk).exists())
        search_book.assert_called_once_with(title="Dune", author="Frank Herbert")
