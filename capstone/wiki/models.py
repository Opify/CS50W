from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# Handles both creation and edits of an article
class Article(models.Model):
    article_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField()
    # 0 means pending, 1 means approved, 2 means rejected
    status = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(2)
    ])

class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment")
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField()