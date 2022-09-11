from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Comment, Genre, TitleGenre, Reviews, Title


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(TitleGenre)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Comment)
