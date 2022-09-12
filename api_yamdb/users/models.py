from tkinter import CASCADE
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


class CodeUser(models.Model):
    user = models.ForeignKey(
        User,
        'Юзер',
        on_delete=CASCADE,
        related_name='code'
    )
    code = models.CharField(
        'Код',
        max_length=40
    )
