import json
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from book.models import History
from book.views import _selected_values


class NavigationViewsTests(TestCase):
    def test_index_is_available_with_get(self) -> None:
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_faq_rejects_post_requests(self) -> None:
        response = self.client.post(reverse("faq"))

        self.assertEqual(response.status_code, 405)

    def test_recommendations_renders_available_books(self) -> None:
        response = self.client.get(reverse("recommendations"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recommendations.html")

    def test_response_requires_at_least_one_reference_book(self) -> None:
        response = self.client.post(reverse("response"), {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selecciona al menos un libro.")

    @patch("book.views._recommend_books", return_value=[])
    def test_response_records_history_for_authenticated_user(
        self, recommend_books: Mock
    ) -> None:
        user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(user)

        response = self.client.post(
            reverse("response"),
            {
                "libro1": "Dune",
                "Fantasía": "Fantasía",
                "Novela": "Novela",
                "message": "A space epic",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(History.objects.filter(user=user, books="Dune").exists())
        recommend_books.assert_called_once()

    def test_mark_as_not_recommended_rejects_invalid_json(self) -> None:
        user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(user)

        response = self.client.post(
            reverse("mark-as-not-recommended"),
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Datos JSON inválidos.")

    @patch("book.views.disliked_book_add")
    def test_mark_as_not_recommended_adds_valid_book(self, disliked_book_add: Mock) -> None:
        user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(user)

        response = self.client.post(
            reverse("mark-as-not-recommended"),
            data=json.dumps({"title": "Dune", "author": "Frank Herbert"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        disliked_book_add.assert_called_once_with(
            user=user, title="Dune", author="Frank Herbert"
        )


class BookViewUtilitiesTests(SimpleTestCase):
    def test_selected_values_ignores_missing_and_blank_values(self) -> None:
        selected = _selected_values(
            {"first": " Dune ", "second": "", "third": "  "},
            ["first", "second", "third"],
        )

        self.assertEqual(selected, ["Dune"])
