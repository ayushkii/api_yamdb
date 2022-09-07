from rest_framework import serializers
from reviews.models import Genre, Category, Title, TitleGenre
import datetime as dt


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'

class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = "__all__"
        model = Title

class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field ='slug', many=True, queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = "__all__"
        model = Title
    
    # def create(self, validated_data):
    #     genres = validated_data.pop('genre')
    #     category = validated_data.pop('category')
    #     title = Title.objects.create(**validated_data)
    #     for genre in genres:
    #         current_genre, status = Genre.objects.get_or_create(**genre)
    #         TitleGenre.objects.create(genre=current_genre, title=title)
    #     Category.objects.get_or_create(**category)
    #     return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте правильность введенного года!')
        return value


# class TitleSerializer(serializers.ModelSerializer):
#     genre = GenreSerializer(many=True)
#     category = CategorySerializer()

#     class Meta:
#         fields = "__all__"
#         model = Title
    
#     def create(self, validated_data):
#         genres = validated_data.pop('genre')
#         category = validated_data.pop('category')
#         title = Title.objects.create(**validated_data)
#         for genre in genres:
#             current_genre, status = Genre.objects.get_or_create(**genre)
#             TitleGenre.objects.create(genre=current_genre, title=title)
#         Category.objects.get_or_create(**category)
#         return title

#     def validate_year(self, value):
#         year = dt.date.today().year
#         if value > year:
#             raise serializers.ValidationError('Проверьте правильность введенного года!')
#         return value

