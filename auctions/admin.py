from django.contrib import admin
from .models import *


class AuctionBidingAdmin(admin.ModelAdmin): 
    list_display = ['bidding_user', 'bidding_on', 'bidding_price', 'bidding_time']


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['watch_user', 'watch_on']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password']


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['auction_user', 'name', 'date','price', 'is_active', 'category']


class AuctionsCommentAdmin(admin.ModelAdmin):
    list_display = ['comment_user', 'comment_on', 'comment','comment_date']


admin.site.register(AuctionBiding, AuctionBidingAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(AuctionComments, AuctionsCommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)

