from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignUpViewSet

router = SimpleRouter()


router.register('', SignUpViewSet)

urlpatterns = [
    path('auth/', include(router.urls)),
]
