from django.db import models
from django.contrib.auth.models import User

class userInformation(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    birthdate = models.DateField()
    preferences = models.TextField(max_length = 300)
    profile_picture = models.ImageField(upload_to='accounts/profile_pics/')
    points = models.PositiveSmallIntegerField()