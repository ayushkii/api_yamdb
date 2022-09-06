from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='имя в url')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name = 'Жанры'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='имя в url')

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(max_length=10000, verbose_name='Описание', null=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre', verbose_name='Жанр', null=True, on_delete =models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="titles", verbose_name="Категория", null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name

class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'