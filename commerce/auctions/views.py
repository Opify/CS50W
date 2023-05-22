from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist


# Task 3 (done)
def index(request):
    listing_set = []
    listings = Listing.objects.all()
    for listing in listings:
        try:
            listing_set.append([listing, Bid.objects.filter(item__id=listing.id).order_by('-current_amount').first()])
        except:
            listing_set.append([listing, None])
    return render(request, "auctions/index.html", {
        "listing_set": listing_set
    })


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


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
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

@login_required
# Task 2 (done)
def create(request):
    if request.method == "POST":
        price = float(request.POST.get("item_price"))
        item = Listing(item_name=request.POST.get("item_name"), item_description=request.POST.get("item_description"), item_category=request.POST.get("item_category"), item_photo=request.POST.get("item_image"), starting_price=price, listing_user=request.user)
        item.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
# Task 4 (done)
def listing(request, id):
    if request.method == "POST":
        bid = float(request.POST.get("bid"))
        item = Listing.objects.get(pk=id)
        try:
            current_amount = Bid.objects.filter(item__id=id).order_by('-current_amount').first().current_amount
        except:
            current_amount = item.starting_price
        if bid > current_amount:
            try:
                record = Bid.objects.filter(item__id=id).order_by('-current_amount').first()
                record.current_amount = bid
                record.bidding_user = request.user
                record.save()
            except:
                record = Bid(current_amount=bid, item=item, bidding_user=request.user)
                record.save()
            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        try:
            item = Listing.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))
        try:
            bid = Bid.objects.filter(item__id=id).first()
        except:
            bid = None
        try:
            comments = Comment.objects.filter(item__id=id).all()
        except:
            comments = None
        if item.listing_user == request.user:
            creator = True
        else:
            creator = False
        if bid == None:
            price = item.starting_price
        else:
            price = bid.current_amount
        minimum = price + 0.01
        try:
            Watchlist.objects.get(pk=id)
            in_watchlist = True
        except:
            in_watchlist = False
        return render(request, "auctions/listing.html", {
            "item": item,
            "bid": bid,
            "comments": comments,
            "creator": creator,
            "price": price,
            "minimum": minimum,
            "in_watchlist": in_watchlist
        })


def comments(request, id):
    if request.method == "POST":
        comment_data = Comment(comment=request.POST.get("comment"))
        comment_data.item = Listing.objects.get(pk=id)
        comment_data.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        return HttpResponseRedirect(reverse("index"))
    

def close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        return HttpResponseRedirect(reverse("index"))


def add_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        watchlist = Watchlist(item=listing, user=request.user)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        return HttpResponseRedirect(reverse("index"))


# Task 5 (done)
def watchlist(request):
    listing_set = []
    listings = Watchlist.objects.all()
    for listing in listings:
        try:
            listing_set.append([listing, Bid.objects.filter(pk=listing.item.id).order_by('-current_amount').first()])
        except:
            listing_set.append([listing, None])
    return render(request, "auctions/watchlist.html", {
        "listing_set": listing_set
    })