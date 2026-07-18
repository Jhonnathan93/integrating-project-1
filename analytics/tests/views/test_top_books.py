from django.test import TestCase
from django.urls import reverse


class TopBooksViewTests(TestCase):
    def test_top_books_defaults_to_all_for_unknown_period(self) -> None:
        response = self.client.get(reverse("top_books_period", args=["unknown"]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["period"], "all")

    def test_top_books_rejects_post_requests(self) -> None:
        response = self.client.post(reverse("top_books"))

        self.assertEqual(response.status_code, 405)
