import csv
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from titles.models import Title, Category, Genre, GenreTitle, Review, Comment


class Command(BaseCommand):
    help = 'Импортирование данных в базу из CSV-файлов'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'model',
            help='Модель для импорта'
        )
        parser.add_argument(
            'csv_file',
            help='Путь к CSV-файлов'
        )

    def handle(self, *args: Any, **options: Any):
        csv_file = options['csv_file']
        model = options['model']

        models = {
            'title': Title,
            'category': Category,
            'genre': Genre,
            'genre_title': GenreTitle,
            'review': Review,
            'comment': Comment
        }

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                models[model].objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
