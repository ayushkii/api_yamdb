from collections import UserString
from secrets import token_hex
from urllib import request

from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import SignUpSerializer, TokenSerializer, code_dict


class PostOnlyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass

class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    def perform_create(self, serializer):
        email = self.request.data['email']
        code = token_hex(16)
        username = self.request.data['username']
        code_dict[f'{username}'] = f'{code}'
        send_mail(
            'код восстановления',
            f'{code}',
            'from@example.com',
            [f'{email}'],
            fail_silently=True,
        )
        serializer.save()

    @action(methods=['post'], detail=False, url_path='token')
    def token(self, request, pk=None):
        refresh = RefreshToken.for_user(request.user)
        response_dict={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_dict, status=status.HTTP_200_OK)

# class TokenViewSet(PostOnlyViewSet):
#     queryset = User.objects.all()
#     serializer_class = TokenSerializer


