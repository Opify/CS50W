from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_timestamp = models.DateTimeField()
    edit_timestamp = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField()
    timestamp = models.DateTimeField()

class Edit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="edit")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edit_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField()
    group = models.CharField(max_length=50)
    
class Following(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

class Group(models.Model):
    interested = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interested_user", blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_group", blank=True, null=True)
    group = models.CharField(max_length=50)
    def __str__(self):
        return f"Group: {self.group}"
