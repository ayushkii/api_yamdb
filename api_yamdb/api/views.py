from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewsSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer, SelfSerializer)
from .permissions import IsAdmin, IsAdminOrReadOnly, AdminModerator
from .filters import TitleFilter


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    """Кастомный вьюсет для модели Genre и Category"""


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AllowAny(),)
        return super().get_permissions()


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AllowAny(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('name')

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return (AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Класс Отзывы для обработки  запросов:
    GET,POST,DELETE,PATCH"""
    serializer_class = ReviewsSerializer
    permission_classes = (AdminModerator,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        id = self.kwargs.get('title_id')
        serializer.save(title_id=id, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс Коментарии для обработки комментариев"""
    serializer_class = CommentSerializer

    permission_classes = (AdminModerator,)
    pagination_class = LimitOffsetPagination


    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)

    @action(methods=['GET', 'PATCH'],
            detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            user = request.user
            serializer = SelfSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,)
        serializer = SelfSerializer(request.user)
        return Response(serializer.data)
