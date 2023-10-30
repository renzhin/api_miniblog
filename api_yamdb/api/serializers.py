import datetime as dt

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import RegexValidator


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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^([-\w]+)$',
                message=' Буквы, цифры и символы @/./+/-/_',
            ),
        ]
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя зарегистрироваться под этим именем!'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^([-\w]+)$',
                message=' Буквы, цифры и символы @/./+/-/_',
            ),
        ]
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя зарегистрироваться под этим именем!'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        confirmation_code = attrs.get("confirmation_code")

        return attrs


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
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title_id', 'pub_date',)
#        validators = [
#            UniqueTogetherValidator(
#                queryset=Review.objects.all(),
#                fields=['author', 'title_id'],
#                message='Нельзя оставить 2 отзыва'
#            )
#        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category'
                  )

    def validate_year(self, value):
        year = dt.date.today().year
        if not (1000 < value <= year):
            raise serializers.ValidationError('Проверьте год создания!')
        return value


class GetTitleSerializer(TitleSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.create(
                genre_id=current_genre, title_id=title)
        return title
