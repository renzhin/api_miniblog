from rest_framework.views import APIView
from rest_framework import viewsets, mixins, generics, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg, F
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api.filtres import TitleFilter
from titles.models import Title, Genre, Category, Review
from api.serializers import (
    SignUpSerializer, TitleSerializer, GetTitleSerializer, GenreSerializer,
    CategorySerializer, UserSerializer, UserCreateSerializer, ReviewSerializer,
    CommentSerializer, CustomTokenObtainSerializer
)
from .permissions import (
    IsAdminPermission, IsAdminUserOrReadOnly, IsAdminOrReadOnly, IsAuthenticatedOrReadOnlydAndAuthor
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class APISignUpUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            # Проверьте, что username и email не пустые
            if username and email:
                user = User.objects.create(
                    username=username,
                    email=email
                )
                confirmation_code = default_token_generator.make_token(user)
                user.confirmation_code = confirmation_code
                user.save()
                send_mail(
                    'Регистрация',
                    f'Это ваш проверочный код: {confirmation_code}.',
                    'yamdb@gmail.ru',
                    [email,],
                    fail_silently=True
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Поле username и email должны быть заполнены'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получите username и confirmation_code из сериализатора
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        # Проверьте, существует ли пользователь с указанным username
        user = User.objects.filter(username=username).first()

        if user and user.confirmation_code == confirmation_code:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


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
