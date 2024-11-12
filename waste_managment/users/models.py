from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Organization


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        unique=False,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        unique=False,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        blank=False,
        null=False,
        unique=True
    )
    organizations = models.ManyToManyField(
        Organization, blank=True, related_name='organizations'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
