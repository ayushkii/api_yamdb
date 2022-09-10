
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from reviews.models import Category, Genre, Reviews, Title
from users.models import User

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewsSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)
from rest_framework import permissions
from .permissions import IsAdmin, IsAdminOrReadOnly, IsSelfUserOrReadOnly
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
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

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
    queryset = Reviews.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс Коментарии для обработки комментариев"""
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Reviews, id=review_id)

        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)

    @action(methods=['get', 'patch'], detail=False, permission_classes=(IsSelfUserOrReadOnly,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


