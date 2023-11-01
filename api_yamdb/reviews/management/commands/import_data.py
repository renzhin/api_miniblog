import csv
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import MyUser

DIRECTORIES_CSV = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    GenreTitle: 'static/data/genre_title.csv',
    MyUser: 'static/data/users.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv'
}

MODELS_COMMAND = {
    'title': Title,
    'category': Category,
    'genre': Genre,
    'genre_title': GenreTitle,
    'review': Review,
    'comment': Comment,
    'user': MyUser,
}


class Command(BaseCommand):
    help = 'Импортирование данных в базу из CSV-файлов'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'model',
            default='all',
            nargs='?',
            help='Модель для импорта'
        )

    def open_file(self, csv_file: str, model: object) -> None:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
                self.stdout.write(self.style.HTTP_INFO('.'), ending='')
                self.stdout.flush()

        self.stdout.write(self.style.SUCCESS('\nДанные успешно загружены из '
                                             f'{DIRECTORIES_CSV[model]}'))

    def handle(self, *args: Any, **options: Any) -> None:
        model_name = options['model']

        if model_name == 'all':
            for model, csv_file in DIRECTORIES_CSV.items():
                self.open_file(csv_file, model)
        else:
            csv_file = DIRECTORIES_CSV[MODELS_COMMAND[model_name]]
            self.open_file(csv_file, MODELS_COMMAND[model_name])
