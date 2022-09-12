from django.urls import path

from .views import signup, token

app_name = 'auth'


urlpatterns = [
    path('signup/', signup),
    path('token/', token),
]
