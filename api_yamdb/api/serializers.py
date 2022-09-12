import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )
        model = Title
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj
        ).aggregate(Avg('score')).get('score__avg')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проверьте правильность'
                'введенного года!'
            )
        return value


class ReviewsSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Невозможно оставить более одного отзыва'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'post', 'id')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=(UniqueValidator(
                    queryset=User.objects.all(),
                    message="Данный email уже существует"
                    ),
                    )
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        lookup_field = 'username'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользовтеля!'
            )
        return value

    def validate_role(self, value):
        if value not in ('admin', 'moderator', 'user'):
            raise serializers.ValidationError(
                'Недопустимая пользовательская роль!'
            )
        return value


class SelfSerializer(UserSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('role',)
        model = User

