from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class NewsletterViewsTests(TestCase):
    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.client.force_login(self.staff_user)

    def test_send_email_to_readers_rejects_get_requests(self) -> None:
        response = self.client.get(reverse("send_email_to_readers"))

        self.assertEqual(response.status_code, 405)

    @patch("newsletter.views.newsletter_send", return_value=2)
    def test_send_email_to_readers_uses_newsletter_service(self, newsletter_send: Mock) -> None:
        response = self.client.post(reverse("send_email_to_readers"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "email_sent_confirmation.html")
        newsletter_send.assert_called_once()
