from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from accounts.models import UserInformation
from accounts.services import user_register
from readinglists.models import ReadingList
from readinglists.services import DEFAULT_LIST_TITLE


class UserRegisterTests(TestCase):
    def test_user_register_creates_profile_and_default_reading_list(self) -> None:
        user = user_register(
            username="reader",
            email="reader@example.com",
            password="secure-password",
            birthdate=date(2000, 1, 1),
            preferences="Science fiction",
        )

        profile = UserInformation.objects.get(user=user)
        default_list = ReadingList.objects.get(user=user, is_default=True)

        self.assertEqual(profile.preferences, "Science fiction")
        self.assertEqual(default_list.title, DEFAULT_LIST_TITLE)
        self.assertTrue(user.check_password("secure-password"))

    def test_user_register_rolls_back_when_username_already_exists(self) -> None:
        User.objects.create_user(username="reader", password="existing-password")

        with self.assertRaises(IntegrityError):
            user_register(
                username="reader",
                email="new@example.com",
                password="secure-password",
                birthdate=date(2000, 1, 1),
                preferences="History",
            )

        self.assertEqual(User.objects.filter(username="reader").count(), 1)
        self.assertEqual(UserInformation.objects.count(), 0)
        self.assertEqual(ReadingList.objects.count(), 0)
