from unittest.mock import Mock, patch

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from book.models import Reader
from newsletter.services import newsletter_send


class NewsletterSendTests(TestCase):
    @override_settings(NEWSLETTER_SENDER_EMAIL="", NEWSLETTER_SENDER_PASSWORD="")
    def test_newsletter_send_requires_sender_configuration(self) -> None:
        with self.assertRaises(ImproperlyConfigured):
            newsletter_send()

    @override_settings(
        NEWSLETTER_SENDER_EMAIL="sender@example.com",
        NEWSLETTER_SENDER_PASSWORD="test-password",
    )
    @patch("newsletter.services.smtplib.SMTP_SSL")
    def test_newsletter_send_uses_smtp_adapter_without_sending_real_email(
        self, smtp_ssl: Mock
    ) -> None:
        Reader.objects.create(id=1, name="First", email="first@example.com")
        Reader.objects.create(id=2, name="Second", email="second@example.com")
        server = smtp_ssl.return_value.__enter__.return_value

        sent_count = newsletter_send()

        self.assertEqual(sent_count, 2)
        server.login.assert_called_once_with("sender@example.com", "test-password")
        self.assertEqual(server.sendmail.call_count, 2)
