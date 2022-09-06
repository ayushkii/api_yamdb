from rest_framework import serializers
from reviews.models import Genre, Category, Title
import datetime as dt


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())

    class Meta:
        fields = "__all__"
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте правильность введенного года!')
        return value

