from django.urls import include, path
from .views import token, signup
# from rest_framework.routers import SimpleRouter

# from .views import SignUpViewSet

# router = SimpleRouter()

app_name = 'auth'

# router.register('signup', SignUpViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
    
# ]

urlpatterns = [
    path('signup/', signup),
    path('token/', token),
]