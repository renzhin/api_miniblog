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


# class NameSlugModel(BaseModel):
#     name = models.CharField(max_length=256, unique=True)
#     slug = models.SlugField(unique=True)

#     class Meta:
#         abstract = True


# class TextAutorModel(BaseModel):
#     text = models.TextField()
#     autor = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name='review', blank=True, null=True
#     )

#     class Meta:
#         abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL)
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
    titile_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )


class Comment(BaseModel):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    review_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='comments'
    )
