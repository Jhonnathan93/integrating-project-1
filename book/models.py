from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description= models.CharField(max_length=250)
    cover = models.URLField()
    author = models.CharField(max_length=100, default= None)
    
    
class Reader(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, default="")
    password = models.CharField(max_length=30, default="j7531594862")
    email = models.EmailField(max_length=50, default="example@example.com")
    age = models.SmallIntegerField(default=0)
    gender = models.CharField(max_length=40, default="Otro")
    points = models.IntegerField(default=0)
    profile_pic = models.CharField(max_length=100, default="https://i.pinimg.com/280x280_RS/42/03/a5/4203a57a78f6f1b1cc8ce5750f614656.jpg")

    def __str__(self):
        return self.name
    


