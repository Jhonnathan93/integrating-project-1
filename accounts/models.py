from django.db import models
from django.contrib.auth.models import User
from book.models import Book
import datetime

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    birthdate = models.DateField(default=datetime.date.today)
    preferences = models.TextField(max_length = 300)
    profile_picture = models.ImageField(upload_to='accounts/profile_pics/')
    points = models.PositiveSmallIntegerField(default=0)
    disliked_books = models.ManyToManyField(Book, related_name='users_who_disliked', blank=True)
