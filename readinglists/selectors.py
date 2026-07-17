from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import ReadingList


def reading_lists_for_user(*, user: User):
    return (
        ReadingList.objects.filter(user=user)
        .prefetch_related("books")
        .order_by("-date_created")
    )


def reading_list_get_for_user(*, user: User, reading_list_id: int) -> ReadingList:
    return get_object_or_404(
        ReadingList.objects.prefetch_related("books"), id=reading_list_id, user=user
    )
