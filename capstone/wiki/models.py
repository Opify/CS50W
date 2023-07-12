from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    expert = models.CharField(max_length=50, blank=True, null=True)

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_timestamp = models.DateTimeField()
    edit_timestamp = models.DateTimeField(blank=True, null=True)
    # 0 means pending, 1 means approved, 2 means rejected
    status = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(2)
    ])
    approving_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}"

class Original_Article(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="original")
    content = models.TextField()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.TextField()
    timestamp = models.DateTimeField()

class Edit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="edit")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edit_user")
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField()
    # 0 means pending, 1 means approved, 2 means rejected
    status = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(2)
    ])
    approving_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True),
    score = models.IntegerField(default=0)
    def __str__(self):
        return f"Status: {self.status}"

class Following_Article(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="following_article")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    def __str__(self):
        return f"Article: {self.article}"
    
class Following_User(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

class Edit_Comment(models.Model):
    edit = models.ForeignKey(Edit, on_delete=models.CASCADE, related_name="edit_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edit_comment_user")
    comment = models.TextField()
    timestamp = models.DateTimeField()

class User_Group(models.Model):
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_expert")
    group = models.CharField(max_length=50)

class Article_Group(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_group")
    group = models.CharField(max_length=50)