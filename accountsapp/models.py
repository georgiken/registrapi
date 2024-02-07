from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=128)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

