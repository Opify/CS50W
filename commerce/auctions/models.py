from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.core import validators


# Task 1 (done)
# despite pass being used, this is actually a complete user model
class User(AbstractUser):
    pass

class Listing(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_category = models.CharField(max_length=100, blank=True)
    item_photo = models.FileField(blank=True)
    starting_price = models.FloatField(default=0, validators=[validators.MinValueValidator(0)])
    def __str__(self):
        return f"Item name: {self.item_name}"

class Bid(models.Model):
    current_amount = models.FloatField(default=0)
    bid_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidding_item_name")
    bid_amount = models.FloatField(default=0)
    def __str__(self):
        return f"Current amount: {self.current_amount}"

class Comment(models.Model):
    comment = models.TextField()
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_item_name")
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Comment: {self.comment}"

# Form Models
class CreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["current_amount"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
