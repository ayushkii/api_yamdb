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
        verbose_name='Юзер',
        on_delete=models.CASCADE,
        related_name='code'
    )
    code = models.CharField(
        'Код',
        max_length=40
    )

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
