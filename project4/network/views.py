from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime

from .models import *


# Tasks 2, 5 (done)
def index(request):
    # Show all posts
    posts = Post.objects.all().order_by('-timestamp')
    paged = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paged.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Task 1 (done)
@login_required
def create_post(request):
    # Handle create post logic
    if request.method == "POST":
        post = Post(username=request.user, content=request.POST["content"], timestamp=datetime.now())
        post.save()
        return HttpResponseRedirect(reverse("index"))
    # Display create post form
    else:
        return render(request, "network/create.html")
    
# Tasks 3, 5 (done)
def profile(request, user):
    # Handle follow logic
    if request.method == "POST":
        try:
            record = Following.objects.filter(following_user=request.user, followed_user=User.objects.get(username=user)).get()
        except:
            follow = Following(following_user = request.user, followed_user=User.objects.get(username=user))
            follow.save()
        else:
            record.delete()
        return HttpResponseRedirect(reverse("profile", args=[user]))
    # Display profile
    else:
        # Checks if username given exists. If invalid, return to index page
        users = User.objects.values()
        for i in range(len(users)):
            if user == users[i]["username"]:
                try:
                    Following.objects.filter(following_user=request.user, followed_user=User.objects.get(username=user)).get()
                except:
                    following = False
                else:
                    following = True
                posts = Post.objects.filter(username=User.objects.get(username=user)).order_by('-timestamp').all()
                paged = Paginator(posts, 10)
                page_number = request.GET.get("page")
                page = paged.get_page(page_number)
                return render(request, "network/profile.html", {
                    "posts": page,
                    "following": following
                })
        return HttpResponseRedirect(reverse("index"))

# Tasks 4, 5 (done)
def following(request):
    # Show all posts from those that user follows
    # Get list of those followed
    followlist = Following.objects.filter(following_user=request.user).values_list('followed_user')
    posts = Post.objects.filter(username__in=followlist).all().order_by('-timestamp')
    paged = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paged.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page
    })