from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class AuctionListing(models.Model):
    auction_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

   

class AuctionBiding(models.Model):
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bidding_on = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, blank=True)
    bidding_price = models.DecimalField(max_digits=10, decimal_places=2)
    bidding_time = models.DateTimeField(auto_now_add=True)



class AuctionComments(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment_on = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.comment_user} commented on {self.comment_on.name}"
    

class Watchlist(models.Model):
    watch_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    watch_on = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, blank=True)

