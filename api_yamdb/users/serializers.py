from urllib import request
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import User

CODE_DICT = {}


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        email = data['email']
        username = data['username']
        if username != 'me':
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким именем или email уже существует')
            return data
        raise serializers.ValidationError(
            'Недопустимое имя пользователя')


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=32)
    username = serializers.CharField(max_length=256)
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        get_object_or_404(User, username=username)
        if CODE_DICT[f'{username}'] == f'{confirmation_code}':
            return data
        raise serializers.ValidationError('Неверный код подтверждения')
