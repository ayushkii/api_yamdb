from django.contrib import admin
from reviews.models import Category, Genre, Title, TitleGenre

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(TitleGenre)
