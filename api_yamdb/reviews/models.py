from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User

RATE_SOCRES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
               (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='имя в url'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='имя в url'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=500,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        max_length=10000,
        verbose_name='Описание',
        null=True,
        blank=False
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        verbose_name="Категория",
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(default=1,
                                             validators=[
                                                 MaxValueValidator(10),
                                                 MinValueValidator(1)
                                             ])
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_author_title_id'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now=True,
    )
    review = models.ForeignKey(
        Review,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
