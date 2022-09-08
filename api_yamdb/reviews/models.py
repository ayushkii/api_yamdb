from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

RATE_SOCRES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class Reviews(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=RATE_SOCRES)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=(
                'title', 'author'
            ),
                name='unique_reviews'
            ),
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Reviews,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='comments',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
