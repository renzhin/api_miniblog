from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
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


class Genre(BaseModel):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(BaseModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    year = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Review(BaseModel):
    text = models.TextField()
    score = models.IntegerField(blank=True, null=True)
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='review', blank=True, null=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review', blank=True, null=True
    )


class Comment(BaseModel):
    text = models.TextField()
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='review', blank=True, null=True
    )
    review = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review', blank=True, null=True
    )
