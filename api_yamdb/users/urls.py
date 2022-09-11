from django.urls import path
from .views import token, signup


app_name = 'auth'


urlpatterns = [
    path('signup/', signup),
    path('token/', token),
]
