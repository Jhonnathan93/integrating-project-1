from django.test import TestCase
from django.urls import reverse


class NavigationViewsTests(TestCase):
    def test_index_is_available_with_get(self) -> None:
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_faq_rejects_post_requests(self) -> None:
        response = self.client.post(reverse("faq"))

        self.assertEqual(response.status_code, 405)
