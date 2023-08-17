from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description= models.CharField(max_length=250)
    cover= models.ImageField(upload_to = 'book/images/')
    
    
class Reader(models.Model):
    name = models.CharField(max_length=100)
    profile_pic= models.ImageField(upload_to = 'book/images/')
    


