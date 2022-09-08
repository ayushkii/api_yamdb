from rest_framework import serializers
from .models import  User

code_dict={}

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)
    
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self,data):
        email=data['email']
        username=data['username']
        if username != 'me':
            if User.objects.filter(username=username,email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким именем или email уже существует')
            return data
        raise serializers.ValidationError(
            'Недопустимое имя пользователя')


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=32)
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        if User.objects.filter(username=data['username']).exists():
            if code_dict[f'{username}'] == f'{confirmation_code}':
                return data
            raise serializers.ValidationError('Неверный код подтверждения')
        raise serializers.ValidationError('Неверное имя пользователя')