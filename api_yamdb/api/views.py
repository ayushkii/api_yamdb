from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins

from .serializers import CommentSerializer, ReviewsSerializer
from reviews.models import Reviews, Title
from .permissions import IsOwnerOrReadOnly


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
