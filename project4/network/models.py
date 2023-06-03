from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Post(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_user")
    content = models.TextField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return f"Username: {self.username}, content: {self.content}, timestamp: {self.timestamp}"
    
class Following(models.Model):
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_user")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_user")
    def __str__(self):
        return f"Follower: {self.following_user}, Following: {self.followed_user}"
    
class Like(models.Model):
    like_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f"Liker: {self.like_user}, Post: {self.post}"