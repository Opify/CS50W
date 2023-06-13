from django.contrib import admin
from django.contrib.auth.models import User

from .models import Article, Comment, Following, Edit_Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Edit_Comment)