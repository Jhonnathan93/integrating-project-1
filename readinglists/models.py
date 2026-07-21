from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from book.models import Book


class ReadingList(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=250)
    cover = models.ImageField(
        upload_to="readinglists/covers/",
        default="readinglist/default_book.png",
        null=True,
        blank=True,
    )
    books = models.ManyToManyField(Book, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("readinglists:detail", args=[str(self.id)])
