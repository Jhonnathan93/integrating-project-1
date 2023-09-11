from django.db import models
from book.models import Book  
from django.contrib.auth.models import User

class ReadingList(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=250)
    cover = models.ImageField(upload_to='readinglists/covers/')
    books = models.ManyToManyField(Book) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 

    def __str__(self):
        return self.title
