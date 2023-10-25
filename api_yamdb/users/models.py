from django.contrib.auth.models import AbstractUser
from django.db import models
# from .validators import UnicodeUsernameValidator

# username_validator = UnicodeUsernameValidator()


class MyUser(AbstractUser):

    USER = 'US'
    MODERATOR = 'MD'
    ADMIN = 'AD'

    ROLE_CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        # validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=USER)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(max_length=150, blank=True)

