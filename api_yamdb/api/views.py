from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleWriteSerializer, TitleReadSerializer

class ListRetrieveCreateDestroyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Кастомный вьюсет для модели Genre и Category"""

class GenreViewSet(ListRetrieveCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination


class CategoryViewSet(ListRetrieveCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    pagination_class = LimitOffsetPagination

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('name')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
