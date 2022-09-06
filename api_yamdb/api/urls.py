from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('categories', CategoryViewSet, basename='category')

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
     
]
