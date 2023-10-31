from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets, mixins, generics, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg, F, Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from api.filtres import TitleFilter
from titles.models import Title, Genre, Category, Review
from api.serializers import (
    TitleSerializer, GetTitleSerializer, GenreSerializer,
    CategorySerializer, UsersSerializer, UserCreateSerializer,
    ReviewSerializer, CommentSerializer, TokenSerializer,
    SignupSerializer  
)
from .permissions import (
    IsAdminPermission, IsAdminUserOrReadOnly, IsAdminOrReadOnly, IsAuthenticatedOrReadOnlydAndAuthor
)

User = get_user_model()


class SignUpView(APIView):
    '''
    POST-запрос с email и username генерирует
    письмо с кодом для получения токена.
    '''
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """Создание пользователя И Отправка письма с кодом."""
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        # Проверяем, существует ли пользователь с таким email или username
        existing_user = User.objects.filter(Q(email=email) | Q(username=username)).first()

        if existing_user:
            # Если пользователь уже существует, генерируем код подтверждения
            confirmation_code = default_token_generator.make_token(existing_user)
            existing_user.confirmation_code = confirmation_code
            existing_user.save()

            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email=settings.AUTH_EMAIL,
                recipient_list=(existing_user.email,),
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Если пользователь не существует, создаем нового пользователя
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email=settings.AUTH_EMAIL,
                recipient_list=(user.email,),
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=(IsAuthenticated,))
    def about_me(self, request):
        if request.method == 'PATCH':
            serializer = UserCreateSerializer(
                request.user, data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserCreateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    '''
    POST-запрос с username и confirmation_code
    возвращает JWT-токен.
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Неверный код')
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg(F('reviews__score'))).order_by('name')


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnlydAndAuthor]
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    permission_classes = [IsAuthenticatedOrReadOnlydAndAuthor]
    http_method_names = ['get', 'post', 'patch', 'delete']

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
