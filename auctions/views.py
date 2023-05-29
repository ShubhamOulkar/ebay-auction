from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionBiding, AuctionComments, AuctionListing, Category, Watchlist
from .model_forms import CreateListingForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



def index(request):
    listing = AuctionListing.objects.all().order_by('-date')
    return render(request, "auctions/index.html",{"listing": listing})


def my_listing(request):
    listing = AuctionListing.objects.filter(auction_user=request.user)
    return render(request, "auctions/my_listing.html", {"listing":listing})


def category_listing(request):
    categories = Category.objects.all()
    listing = AuctionListing.objects.all()
    actives = []
    inactives = []
    for category in categories:
        auction_by_category = listing.filter(is_active=True, category=category)
        count =  auction_by_category.count()
        actives.append(
            {"category": category,
            "auctions": [{'name':auction.name, 'id':auction.pk} for auction in auction_by_category],
            "count": count,
            },)
        
    for category in categories:
        auction_by_category = listing.filter(is_active=False, category=category)
        count =  auction_by_category.count()
        inactives.append(
            {"category": category,
            "auctions": [{'name':auction.name, 'id':auction.pk} for auction in auction_by_category],
            "count": count,
            },)
    
    actives = sorted(actives, key=actives.count, reverse=True)
    inactives = sorted(inactives, key=inactives.count, reverse=True)
    return render(request, "auctions/category_listing.html",
                  {"actives":actives, "inactives":inactives,})
                  

def details(request, pk):
    auction = AuctionListing.objects.get(pk=pk)
    bid_count = AuctionBiding.objects.filter(bidding_on=auction.id).count()
    # ! Bidding Details
    if request.user.is_authenticated:
        check_user_bidding = AuctionBiding.objects.filter(bidding_user=request.user,bidding_on=auction.id)
        if not check_user_bidding:
            msg = "You are not bidded on this auction. Please do it now."
            user_last_bid_amount = 0
            user_bid_count = 0
        else:
            msg = ''
            user_bid_count = check_user_bidding.count()
            user_last_bid_amount = check_user_bidding.order_by('-bidding_time').first().bidding_price
    else:
        msg = "Login/Register for a bid."
        user_last_bid_amount = 0
        user_bid_count = 0

    # ! Comment details
    comments = AuctionComments.objects.filter(comment_on=auction.id)

    # ! Watchlist details
    if request.user.is_authenticated:
        try:
            Watchlist.objects.get(watch_user=request.user, watch_on=pk)
            watchlist = True
        except Watchlist.DoesNotExist:
            watchlist = False
    else:
        watchlist = False

    # ! bid winner details
    if not auction.is_active :
        winner = AuctionBiding.objects.filter(bidding_on=pk).order_by('-bidding_price').first()
    else: 
        winner = "Winner Will be updated after auction closed."

    return render(request, "auctions/details.html",
                  {"auction": auction,
                    "count":bid_count,
                    "comments": comments,
                    "watchlist": watchlist,
                    "msg":msg,
                    "user_bid_count": user_bid_count,
                    "user_last_bid_amount": user_last_bid_amount,
                    "winner":winner,
                    })


@login_required(login_url='login')
def add_watchlist(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    objW = Watchlist()
    objW.watch_on = listing
    objW.watch_user = request.user
    objW.save()

    return HttpResponseRedirect(reverse("details", args=(pk, )))


@login_required(login_url='login')
def remove_watchlist(request, pk):
    Watchlist.objects.filter(watch_user=request.user, watch_on=pk).delete()
    return HttpResponseRedirect(reverse("details", args=(pk, )))


@login_required(login_url='login')
def inactive(request, pk):
    auction = AuctionListing.objects.get(pk=pk)
    if request.user == auction.auction_user:
        auction.is_active = False
        auction.save()
        return HttpResponseRedirect(reverse("details", args=(pk, )))
    else:
        return HttpResponse('Not allowed')


@login_required(login_url='login')
def active(request, pk):
    auction = AuctionListing.objects.get(pk=pk)
    if request.user == auction.auction_user:
        auction.is_active = True
        auction.save()
        return HttpResponseRedirect(reverse("details", args=(pk, )))
    else:
        return HttpResponse('Not allowed')


def do_bid(request, pk):
    listing = AuctionListing.objects.get(pk=pk)
    old_bid = AuctionBiding.objects.filter(bidding_on=pk)
    max_old_bid = old_bid.order_by('-bidding_price').first()

    if not old_bid:
        old_price = listing.price
    else:
        old_price = max_old_bid.bidding_price

    if request.method == 'POST':
        bid = request.POST['bid']
        if listing.is_active:
            if float(bid) > old_price and float(bid) > listing.price:
                objW = AuctionBiding()
                objW.bidding_on = listing
                objW.bidding_user = request.user
                objW.bidding_price = float(bid)
                objW.save()
                messages.success(request, "Bid is saved successfully.")
            else:
                messages.warning(request,f"Your bid is less than maximum bidder price ${old_price}/bidding starting price, please increase bidding price.")
        else:
            messages.warning(request,"Your bid is not saved because auction is closed")
    return HttpResponseRedirect(reverse("details", args=(pk, )),)
        

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.auction_user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
        return render(request, "auctions/create_listing.html", {'form':form})


@login_required(login_url='login')
def add_category(request):
    if request.method == "POST":
        new_category = request.POST['new-category']
        db_category = Category()
        db_category.category = new_category
        db_category.save()
        return HttpResponseRedirect(reverse("create_listing"))
    return render(request, "auctions/add_category.html")
                  

class EditListing(LoginRequiredMixin, UpdateView):
    model = AuctionListing
    form_class = CreateListingForm
    template_name = "auctions/edit_listing.html"
    success_url = reverse_lazy('index')


class DeleteListing(LoginRequiredMixin,DeleteView):
    model = AuctionListing
    success_url = reverse_lazy('index')
    template_name = "auctions/delete_listing.html"
    

def add_comment(request,pk):
    if request.method == 'POST':
        new_comment = request.POST['comment']
        comment_db = AuctionComments()
        comment_db.comment_user = request.user
        comment_db.comment_on = AuctionListing.objects.get(pk=pk)
        comment_db.comment = new_comment
        comment_db.save()
    return HttpResponseRedirect(reverse("details", args=(pk, )),)


def watchlist(request):
    watch_list = Watchlist.objects.filter(watch_user=request.user)
    return render(request,"auctions/watchlist.html", {'watch_list': watch_list})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # ensure username and email is filled in
        if username == '' or email == '':
            return render(request, "auctions/register.html", {
                "message": "Please enter username and/or email."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password == '' or confirmation == '':
            return render(request, "auctions/register.html", {
                "message": "Empty password field is not acceptable."
            })
        elif password != confirmation: 
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
