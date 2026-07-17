from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from book.models import Book


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(default=timezone.localdate)
    preferences = models.TextField(max_length=300)
    profile_picture = models.ImageField(upload_to="accounts/profile_pics/", blank=True)
    points = models.PositiveSmallIntegerField(default=0)
    disliked_books = models.ManyToManyField(Book, related_name="users_who_disliked", blank=True)

    def __str__(self) -> str:
        return self.user.username
