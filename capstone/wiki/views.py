from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
import markdown

from . import util
from .models import *


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-timestamp').all()
    return render(request, "wiki/index.html", {
        "articles": articles
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
            return render(request, "wiki/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "wiki/login.html")

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
            return render(request, "wiki/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "wiki/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "wiki/register.html")

@login_required
def create(request):
    # handle article creation
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        try:
            Article.objects.filter(title=title).get()
        except:
            article = Article(article_user=request.user, title=title, content=content, timestamp=datetime.now())
            article.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    # handle getting to form
    else:
        return render(request, "wiki/create.html")

def article(request, title):
    try:
        article = Article.objects.filter(title=title).get()
    except:
        return HttpResponseRedirect(reverse("index"))
    else:
        content = markdown.markdown(article.content)
        return render(request, "wiki/article.html", {
            "article": article,
            "content": content
        })
