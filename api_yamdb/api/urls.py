from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import CommentViewSet, ReviewsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
=======
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet)

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

>>>>>>> test
