from secrets import token_hex

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CodeUser, User
from .serializers import SignUpSerializer, TokenSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data['email']
        code = token_hex(16)
        send_mail(
            'код восстановления',
            f'{code}',
            'from@example.com',
            [f'{email}'],
            fail_silently=True,
        )
        serializer.save()
        user = get_object_or_404(User, username=request.data['username'])
        CodeUser.objects.create(user=user, code=code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        response_dict = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
