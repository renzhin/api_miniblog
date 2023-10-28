from rest_framework import viewsets, mixins, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from titles.models import Title, Genre, Category, Review
from api.serializers import (
    SignUpSerializer, TitleSerializer, GetTitleSerializer, GenreSerializer,
    CategorySerializer, UserSerializer, ReviewSerializer, CommentSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ('username',)
    lookup_field = 'username'


class APISignUpUser(APIView):
    permission_classes = [AllowAny,]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = User.objects.create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Регистрация',
            f'Это ваш проверочный код: {confirmation_code}.',
            'yamdb@gmail.ru',
            [email,],
            fail_silently=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.http_method_names == 'GET':
            return GetTitleSerializer
        return TitleSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg(F('reviews__score')))


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        """Получение экземпляра Title по title_id."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Переопределение queryset."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Заполнение полей author и post."""
        title = self.get_title()
        serializer.save(author=self.request.user, title_id=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        """Получение экземпляра Title по title_id."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Переопределение queryset."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Заполнение полей author и post."""
        review = self.get_review()
        serializer.save(author=self.request.user, review_id=review)
