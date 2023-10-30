from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class MyUser(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^([-\w]+)$',
                message=' Буквы, цифры и символы @/./+/-/_',
            ),
        ]
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254,
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=150,
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    @property
    def is_admin(self):
        return self.is_staff or self.role == MyUser.ADMIN

    @property
    def is_moderator(self):
        return self.role == MyUser.MODERATOR

    def __str__(self):
        return self.username
