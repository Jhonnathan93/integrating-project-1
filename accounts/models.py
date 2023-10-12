from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Agrega campos personalizados
    gender = models.CharField(max_length=10, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='accounts/profile_pics/', null=True, blank=True)
