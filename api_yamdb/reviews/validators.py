import datetime as dt

from django.core.validators import RegexValidator
from rest_framework import serializers


def validate_me(value):
    if value == 'me':
        raise serializers.ValidationError('Имя пользователя "me" запрещено.')


def validate_year(self, value):
    year = dt.date.today().year
    if not (1000 < value <= year):
        raise serializers.ValidationError('Проверьте год создания!')
    return value


username_validator = RegexValidator(
    regex=r'^([-\w]+)$',
    message='Буквы, цифры и символы @/./+/-/_',
)
