from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    price = models.IntegerField(default=0)
    image_url = models.URLField(max_length=200, default=None)
    date = models.DateTimeField(default=timezone.now)
    categories = models.CharField(max_length=64, blank=True, null=True, default="")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_user')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'
    
class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid_listing')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_user')
    bid = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

class Comments(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment_listing')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")