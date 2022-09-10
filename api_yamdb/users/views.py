from secrets import token_hex
from tokenize import Token
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import SignUpSerializer, TokenSerializer, CODE_DICT


# class PostOnlyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     pass

# class SignUpViewSet(PostOnlyViewSet):
#     queryset = User.objects.all()
#     serializer_class = SignUpSerializer
#     def perform_create(self, serializer):
#         email = self.request.data['email']
#         code = token_hex(16)
#         username = self.request.data['username']
#         code_dict[f'{username}'] = f'{code}'
#         send_mail(
#             'код восстановления',
#             f'{code}',
#             'from@example.com',
#             [f'{email}'],
#             fail_silently=True,
#         )
#         serializer.save()

#     @action(methods=['post'], detail=False, url_path='token')
#     def token(self, request, pk=None):
#         refresh = RefreshToken.for_user(request.user)
#         response_dict={
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#         return Response(response_dict, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data['email']
        code = token_hex(16)
        username = request.data['username']
        CODE_DICT[f'{username}'] = f'{code}'
        send_mail(
            'код восстановления',
            f'{code}',
            'from@example.com',
            [f'{email}'],
            fail_silently=True,
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, request.data['username'])
        refresh = RefreshToken.for_user(user)
        response_dict={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
