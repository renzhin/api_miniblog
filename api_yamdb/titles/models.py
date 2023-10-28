from django.db import models
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата добавления'
    )

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

    def str(self):
        return f'{self.genre} {self.title}'


class Review(BaseModel):
    text = models.TextField()
    score = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(BaseModel):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
