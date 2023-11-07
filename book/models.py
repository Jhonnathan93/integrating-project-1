from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
TIME_ZONE = 'America/Bogota'


class Book(models.Model):
    isbn = models.CharField(max_length=13, default="N/A")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default="Sin descripción disponible")
    year_publication = models.IntegerField(default=0)
    topics = models.CharField(max_length=120, default="N/A")
    rating = models.FloatField(default=0)
    cover = models.URLField(default="https://user-images.githubusercontent.com/140737841/280489450-728d5fb6-442e-4912-bed3-f0a5689fbdec.png")
    buy_link = models.URLField(default="https://books.google.com.co/books?uid=117901420878484918404&hl=es")
    author = models.CharField(max_length=100, default= None)
    disliked_by = models.ManyToManyField('accounts.userInformation', related_name='books_disliked_by_users', blank=True)
    dateAdded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Reader(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=40, default="")
    password = models.CharField(max_length=30, default="j7531594862")
    email = models.EmailField(max_length=50, default="example@example.com")
    age = models.SmallIntegerField(default=0)
    gender = models.CharField(max_length=40, default="Otro")
    points = models.IntegerField(default=0)
    profile_pic = models.CharField(max_length=100, default="https://i.pinimg.com/280x280_RS/42/03/a5/4203a57a78f6f1b1cc8ce5750f614656.jpg")

    def __str__(self):
        return self.name
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.CharField(max_length=160)
    topics = models.CharField(max_length=66)
    genres = models.CharField(max_length=38)
    date = models.DateTimeField(default=timezone.now)

