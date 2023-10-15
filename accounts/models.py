from django.db import models

# Create your models here.

class Readers(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    age = models.SmallIntegerField(blank=True, null=True)
    gender = models.BooleanField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
