# abstract_user/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        default='user',
    )

# class PreUser(models.Model):
#     email = models.EmailField(max_length=254)
#     username = models.CharField(max_length=150)
#     code = models.CharField(max_length=150)

