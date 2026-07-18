from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import UserInformation
from readinglists.models import ReadingList


class AuthenticationViewsTests(TestCase):
    def test_signup_get_renders_form(self) -> None:
        response = self.client.get(reverse("accounts:signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_signup_creates_account_and_authenticates_user(self) -> None:
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "new-reader",
                "email": "reader@example.com",
                "password1": "secure-password",
                "password2": "secure-password",
                "birthdate": "2000-01-01",
                "preferences": "Fantasy",
            },
        )

        user = User.objects.get(username="new-reader")
        self.assertRedirects(response, reverse("home"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertTrue(UserInformation.objects.filter(user=user).exists())
        self.assertTrue(ReadingList.objects.filter(user=user, is_default=True).exists())

    def test_signup_rejects_mismatched_passwords(self) -> None:
        response = self.client.post(
            reverse("accounts:signup"),
            {"password1": "one", "password2": "two"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Las contraseñas no coinciden.")
        self.assertEqual(User.objects.count(), 0)

    def test_login_authenticates_valid_credentials(self) -> None:
        User.objects.create_user(username="reader", password="secure-password")

        response = self.client.post(
            reverse("accounts:login"),
            {"usuario": "reader", "contraseña": "secure-password"},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_profile_requires_authentication(self) -> None:
        response = self.client.get(reverse("accounts:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
