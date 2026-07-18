from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserInformation
from accounts.services import profile_update


class ProfileUpdateTests(TestCase):
    def test_profile_update_changes_username_and_preferences(self) -> None:
        user = User.objects.create_user(username="before", password="password")
        profile = UserInformation.objects.create(user=user, preferences="Before")

        updated_profile = profile_update(
            profile=profile,
            username="after",
            preferences="After",
        )

        user.refresh_from_db()
        updated_profile.refresh_from_db()
        self.assertEqual(user.username, "after")
        self.assertEqual(updated_profile.preferences, "After")
