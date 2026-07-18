from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.urls import reverse

from accounts.models import UserInformation
from readinglists.models import ReadingList


@tag("integration")
class UserLifecycleIntegrationTests(TestCase):
    def test_registration_creates_profile_default_list_and_authenticated_session(
        self,
    ) -> None:
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "integration-reader",
                "email": "reader@example.com",
                "password1": "secure-password",
                "password2": "secure-password",
                "birthdate": "2000-01-01",
                "preferences": "Science fiction",
            },
        )

        user = User.objects.get(username="integration-reader")
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
        self.assertTrue(UserInformation.objects.filter(user=user).exists())
        self.assertTrue(ReadingList.objects.filter(user=user, is_default=True).exists())

    def test_login_profile_update_and_logout_persist_the_user_lifecycle(self) -> None:
        user = User.objects.create_user(
            username="reader", email="reader@example.com", password="secure-password"
        )
        profile = UserInformation.objects.create(user=user, preferences="Fantasy")

        login_response = self.client.post(
            reverse("accounts:login"),
            {"usuario": "reader", "contraseña": "secure-password"},
        )
        profile_response = self.client.get(reverse("accounts:profile"))
        update_response = self.client.post(
            reverse("accounts:editprofile"),
            {"username": "updated-reader", "preferences": "Mystery"},
        )
        logout_response = self.client.get(reverse("accounts:logout"))

        user.refresh_from_db()
        profile.refresh_from_db()
        self.assertRedirects(login_response, reverse("home"))
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(update_response.status_code, 302)
        self.assertEqual(update_response["Location"], reverse("accounts:profile"))
        self.assertEqual(user.username, "updated-reader")
        self.assertEqual(profile.preferences, "Mystery")
        self.assertRedirects(logout_response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)
