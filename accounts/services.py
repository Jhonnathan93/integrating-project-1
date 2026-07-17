from datetime import date

from django.contrib.auth.models import User
from django.db import transaction

from .models import UserInformation


@transaction.atomic
def user_register(
    *,
    username: str,
    email: str,
    password: str,
    birthdate: date,
    preferences: str,
    profile_picture=None,
) -> User:
    user = User.objects.create_user(username=username, email=email, password=password)
    UserInformation.objects.create(
        user=user,
        birthdate=birthdate,
        preferences=preferences,
        profile_picture=profile_picture,
    )

    from readinglists.services import reading_list_create_default

    reading_list_create_default(user=user)
    return user


@transaction.atomic
def profile_update(
    *, profile: UserInformation, username: str, preferences: str, profile_picture=None
) -> UserInformation:
    user = profile.user
    if username and username != user.username:
        user.username = username
        user.full_clean(exclude=["password"])
        user.save(update_fields=["username"])
    profile.preferences = preferences
    update_fields = ["preferences"]
    if profile_picture:
        profile.profile_picture = profile_picture
        update_fields.append("profile_picture")
    profile.full_clean()
    profile.save(update_fields=update_fields)
    return profile
