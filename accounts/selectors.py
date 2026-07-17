from django.contrib.auth.models import User

from .models import UserInformation


def user_profile_get(*, user: User) -> UserInformation:
    return UserInformation.objects.select_related("user").get(user=user)
