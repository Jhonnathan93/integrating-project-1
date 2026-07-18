import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from readinglists.models import ReadingList


class ReadingListViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="reader", password="password")
        self.client.force_login(self.user)

    def test_overview_lists_authenticated_users_lists(self) -> None:
        ReadingList.objects.create(
            user=self.user, title="Favorites", description="Description"
        )

        response = self.client.get(reverse("overview"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "overview.html")
        self.assertEqual(list(response.context["readinglists"]), list(ReadingList.objects.all()))

    def test_create_list_persists_valid_submission(self) -> None:
        response = self.client.post(
            reverse("createlist"),
            {"title": "Favorites", "description": "Books to revisit"},
        )

        reading_list = ReadingList.objects.get(user=self.user, title="Favorites")
        self.assertRedirects(response, reverse("detail", args=[reading_list.id]))

    def test_add_to_reading_list_rejects_invalid_json(self) -> None:
        response = self.client.post(
            reverse("add-to-list"),
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Datos JSON inválidos.")

    def test_add_to_reading_list_creates_default_list_and_book(self) -> None:
        response = self.client.post(
            reverse("add-to-list"),
            data=json.dumps({"title": "Dune", "author": "Frank Herbert"}),
            content_type="application/json",
        )

        default_list = ReadingList.objects.get(user=self.user, is_default=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(default_list.books.count(), 1)
