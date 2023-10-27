# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=10, unique=True)
    profile_img = models.ImageField(
        upload_to='accounts/profile/', blank=True, null=True)
    introduce = models.TextField(max_length=500, null=True, blank=True)
