import json
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from book.models import Book
from readinglists.models import ReadingList


class ReadingListViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(self.user)

    def test_overview_lists_authenticated_users_lists(self) -> None:
        ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )

        response = self.client.get(reverse("readinglists:overview"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "overview.html")
        self.assertEqual(
            list(response.context["readinglists"]), list(ReadingList.objects.all())
        )

    def test_create_list_persists_valid_submission(self) -> None:
        response = self.client.post(
            reverse("readinglists:createlist"),
            {"title": "Favorites", "description": "Books to revisit"},
        )

        reading_list = ReadingList.objects.get(user=self.user, title="Favorites")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"], reverse("readinglists:detail", args=[reading_list.id])
        )

    def test_create_list_shows_validation_error_for_missing_data(self) -> None:
        response = self.client.post(reverse("readinglists:createlist"), {"title": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El título y la descripción son obligatorios.")

    def test_add_to_reading_list_rejects_invalid_json(self) -> None:
        response = self.client.post(
            reverse("readinglists:add-to-list"),
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Datos JSON inválidos.")

    def test_add_to_reading_list_creates_default_list_and_book(self) -> None:
        response = self.client.post(
            reverse("readinglists:add-to-list"),
            data=json.dumps({"title": "Dune", "author": "Frank Herbert"}),
            content_type="application/json",
        )

        default_list = ReadingList.objects.get(user=self.user, is_default=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(default_list.books.count(), 1)

    def test_detail_shows_reading_list_for_owner(self) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )

        response = self.client.get(
            reverse("readinglists:detail", args=[reading_list.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Favorites")

    def test_detail_rejects_submission_without_title_or_author(self) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )

        response = self.client.post(
            reverse("readinglists:detail", args=[reading_list.id]), {}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El título y el autor son obligatorios.")

    def test_update_reading_list_persists_valid_submission(self) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Before", description="Before description"
        )

        response = self.client.post(
            reverse("readinglists:updatereadinglist", args=[reading_list.id]),
            {"title": "After", "description": "After description"},
        )

        reading_list.refresh_from_db()
        self.assertRedirects(
            response, reverse("readinglists:detail", args=[reading_list.id])
        )
        self.assertEqual(reading_list.title, "After")

    def test_delete_list_removes_non_default_list(self) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )

        response = self.client.post(
            reverse("readinglists:deletelist", args=[reading_list.id])
        )

        self.assertRedirects(response, reverse("readinglists:overview"))
        self.assertFalse(ReadingList.objects.filter(pk=reading_list.id).exists())

    def test_delete_book_removes_book_from_list(self) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )
        book = Book.objects.create(title="Dune", author="Frank Herbert")
        reading_list.books.add(book)

        response = self.client.post(
            reverse("readinglists:deletebook", args=[reading_list.id, book.id])
        )

        self.assertRedirects(
            response, reverse("readinglists:detail", args=[reading_list.id])
        )
        self.assertFalse(reading_list.books.filter(pk=book.id).exists())

    @patch("readinglists.views.search_book")
    def test_detail_adds_book_found_by_provider(self, search_book: Mock) -> None:
        reading_list = ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )
        search_book.return_value = {
            "title": "Dune",
            "author": "Frank Herbert",
            "description": "Description",
            "cover": "https://example.com/dune.jpg",
            "buy_link": "https://example.com/dune",
        }

        response = self.client.post(
            reverse("readinglists:detail", args=[reading_list.id]),
            {"title": "Dune", "author": "Frank Herbert"},
        )

        self.assertRedirects(
            response, reverse("readinglists:detail", args=[reading_list.id])
        )
        self.assertEqual(reading_list.books.count(), 1)
