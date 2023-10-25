from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):

    USER = 'US'
    MODERATOR = 'MD'
    ADMIN = 'AD'

    ROLE_CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=150, blank=True)
