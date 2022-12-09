from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    gender = models.CharField(max_length=10, default='male', choices=GENDER_CHOICES)
    location = models.CharField(max_length=210)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'gender', 'location']