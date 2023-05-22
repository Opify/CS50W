from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



# Task 1 (done)
# despite pass being used, this is actually a complete user model
class User(AbstractUser):
    pass

class Listing(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_category = models.CharField(max_length=100, blank=True)
    item_photo = models.CharField(max_length=100, blank=True)
    starting_price = models.FloatField()
    closed = models.BooleanField(default=False)
    listing_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Item id: {self.id}, Listing User: {self.listing_user}"

class Bid(models.Model):
    current_amount = models.FloatField(default=0)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidding_item_name")
    bidding_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Current amount: {self.current_amount}, Bidding User: {self.bidding_user}"
    class Meta:
        ordering=["-current_amount"]

class Comment(models.Model):
    comment = models.TextField()
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_item_name")
    def __str__(self):
        return f"Comment: {self.comment}, Item: {self.item}"

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_item_name")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"Item name: {self.item}, User: {self.user}"
