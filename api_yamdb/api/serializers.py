import datetime as dt

from rest_framework import serializers
from django.contrib.auth import get_user_model

from titles.models import Category, Genre, Title, GenreTitle, Comment, Review

User = get_user_model()

CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review_id', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title_id', 'pub_date',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(slug_field='name')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return 0

    def validate_year(self, value):
        year = dt.date.today().year
        if not (1000 < value <= year):
            raise serializers.ValidationError('Проверьте год создания!')
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.create(
                genre_id=current_genre, title_id=title)
        return title
