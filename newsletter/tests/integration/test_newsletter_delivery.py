from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from book.models import Reader


@tag("integration")
@override_settings(
    NEWSLETTER_SENDER_EMAIL="newsletter@example.com",
    NEWSLETTER_SENDER_PASSWORD="test-password",
)
class NewsletterDeliveryIntegrationTests(TestCase):
    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            username="staff", password="secure-password", is_staff=True
        )
        self.client.force_login(self.staff_user)
        Reader.objects.create(name="Newsletter reader", email="reader@example.com")

    @patch("newsletter.services.smtplib.SMTP_SSL")
    def test_staff_delivery_uses_smtp_for_persisted_recipients(
        self, smtp_ssl: Mock
    ) -> None:
        smtp_server = smtp_ssl.return_value.__enter__.return_value

        response = self.client.post(reverse("send_email_to_readers"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "email_sent_confirmation.html")
        smtp_server.login.assert_called_once_with(
            "newsletter@example.com", "test-password"
        )
        smtp_server.sendmail.assert_called_once()
        self.assertEqual(
            smtp_server.sendmail.call_args.args[:2],
            ("newsletter@example.com", "reader@example.com"),
        )
