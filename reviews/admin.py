from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(TitleGenre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
