from django.contrib.auth.models import AbstractUser
from django.db import models


# Task 1
# despite pass being used, this is actually a complete user model
class User(AbstractUser):
    pass

class Listings(models.Model):
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    def __str__(self):
        return f"Item name: {self.item_name}"

class Bids(models.Model):
    current_amount = models.FloatField()
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    def __str__(self):
        return f"Current amount: {self.current_amount}"

class Comments(models.Model):
    comment = models.TextField()
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Comment: {self.comment}"

