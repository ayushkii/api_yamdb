from django.urls import path, include
from .views import SignUpViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()


router.register('', SignUpViewSet)

urlpatterns = [
    path('auth/', include(router.urls)),
]
