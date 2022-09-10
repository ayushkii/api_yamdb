from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignUpViewSet

router = SimpleRouter()

app_name = 'auth'

router.register('', SignUpViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
