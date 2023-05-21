from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


# Task 3 (done)
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
# Task 2
def create(request):
    if request.method == "POST":
       price = float(request.POST.get("item_price"))
       item = Listing(item_name=request.POST.get("item_name"), item_description=request.POST.get("item_description"), item_category=request.POST.get("item_category"), item_photo=request.POST.get("item_image"), starting_price=price, listing_user=request.user)
       item.save()
       return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
# Task 4
def listing(request, id):
    if request.method == "POST":
        pass
    else:
        item = Listing.objects.get(pk=id)
        bid = Bid.objects.get(pk=id)
        comments = Comment.objects.get(pk=id)
        if request.user.is_authenticated:
            if item.listing_user == request.user.username:
                creator = True
            else:
                creator = False
        if not bid:
            price = item.starting_price
        else:
            price = bid.current_amount
        return render(request, "auctions/listing.html", {
            "item": item,
            "bid": bid,
            "comments":comments,
            "creator":creator,
            "price":price
        })