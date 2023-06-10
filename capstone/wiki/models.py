from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# Handles both creation and edits of an article
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_timestamp = models.DateTimeField()
    edit_timestamp = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"Content: {self.content}"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField()

class Edit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="edit")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="edit_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField()
    # 0 means pending, 1 means approved, 2 means rejected
    status = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(2)
    ])
    approving_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

class Following(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="following")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_user")
 