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
import re

from . import util
from .models import *


# Display all articles
def index(request):
    articles = Article.objects.order_by('-create_timestamp').all()
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
        # checks if article already exists via title
        try:
            Article.objects.filter(title=title).get()
        except:
            article = Article(user=request.user, title=title, content=content, create_timestamp=datetime.now())
            article.save()
            original = Original_Article(article=Article.objects.filter(title=title).get(), content=content)
            original.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    # handle getting to form
    else:
        return render(request, "wiki/create.html")

# Display article and coments
def article(request, title):
    try:
        article = Article.objects.filter(title=title).get()
    except:
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            comments = Comment.objects.filter(article=article).order_by('-timestamp').all()
        except:
            comments = None
        content = markdown.markdown(article.content)
        return render(request, "wiki/article.html", {
            "article": article,
            "content": content,
            "comments": comments
        })

# Display lists of edits for an article
def edits(request, title):
    try:
        article = Article.objects.filter(title=title).get()
        edits = Edit.objects.filter(article=article).order_by('-timestamp').all()
    except:
        return HttpResponseRedirect(reverse("article", args=[title]))
    else:
        changes = []
        for edit in edits:
            list = []
            list.append(edit)
            list.append(util.track_changes(article.content, edit.content))
            changes.append(list)
        # if you're wondering how each change is stored, index 0 is the edit itself, index 1 is the list used to display changes made
        return render(request, "wiki/edits.html", {
            "changes": changes,
            "title": title
        })

@login_required
# handle edits
def edit(request, title):
    # handle edit logic
    if request.method == "POST":
        try:
            article = Article.objects.filter(title=title).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            edit = Edit(article=article, user=request.user, title=request.POST.get("title"), content=request.POST.get("content"), timestamp=datetime.now(), status = 0)
            edit.save()
            return HttpResponseRedirect(reverse("article", args=[title]))
    # handle edit page
    else:
        try:
            article = Article.objects.filter(title=title).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "wiki/edit.html", {
                "article": article
            })

# Display view edits and approval/rejection
def edit_view(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        action = body.get("action")
        edit = Edit.objects.get(pk=id)
        if action == "accept":
            edit.status = 1
            edit.approving_user = request.user
            content = edit.content
            timestamp = datetime.now()
            article = edit.article
            article.content = content
            article.edit_timestamp = timestamp
            edit.save()
            article.save()
            return HttpResponse(200)
        elif action == "reject":
            edit.status = 2
            edit.approving_user = request.user
            edit.save()
            return HttpResponse(200)
        print(f"{action}")
        return HttpResponseRedirect(reverse('edit_view', args=[id]))
    else:
        try:
            edit = Edit.objects.get(pk=id)
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            try:
                edit_comments = Edit_Comment.objects.filter(edit=edit).order_by('-timestamp').all()
            except:
                edit_comments = None
            current_version = Edit.objects.filter(article=edit.article, status=1).order_by('-timestamp').first()
            if current_version != edit:
                current = False
            else:
                current = True
            content = markdown.markdown(edit.content)
            return render(request, "wiki/edit_view.html", {
                "edit": edit,
                "content": content,
                "edit_comments": edit_comments,
                "current": current
            })

# handle following request and getting to following
@login_required
def following(request):
    # handle following page
    if request.method == "GET":
        try:
            following = Following.objects.filter(user=request.user).all()
        except:
            following = None
        return render(request, "wiki/following.html", {
            "following": following
        })
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def follow(request, id):
    # handle following request
    if request.method == "POST":
        try:
            following = Following.objects.filter(article=Article.objects.get(pk=id), user=request.user).get()
        except:
            following = Following(article=Article.objects.get(pk=id), user=request.user)
            following.save()
            return HttpResponse(200)
        else:
            following.delete()
            return HttpResponse(200)
    # check if follow exists
    else:
        try:
            following = Following.objects.filter(article=Article.objects.get(pk=id), user=request.user).get()
        except:
            return JsonResponse({"followed": "false"})
        else:
            return JsonResponse({"followed": "true"})

# handle query results
def query(request):
    query = request.GET["q"]
    articles = Article.objects.values_list('title', flat=True)
    if query in articles:
        return HttpResponseRedirect(reverse("article", args=[query]))
    else:
        suggestions = []
        # use regex to generate list of suggested articles
        for entry in articles:
            if re.search(query, entry) is not None:
                suggestions.append(entry)
        return render(request, "wiki/query.html", {
            "results": suggestions
        })

@login_required    
# handle uploading comments from articles
def comment(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        content = body.get("comment")
        timestamp = datetime.now()
        user = request.user
        comment = Comment(article=Article.objects.get(pk=id), user=user, comment=content, timestamp=timestamp)
        comment.save()
        return JsonResponse({"timestamp": timestamp.strftime('%B %d, %Y, %I:%M %p'), "user": request.user.username})
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
# handle uploading comments from edits
def edit_comment(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        content = body.get("edit_comment")
        timestamp = datetime.now()
        user = request.user
        comment = Edit_Comment(edit=Edit.objects.get(pk=id), user=user, comment=content, timestamp=timestamp)
        comment.save()
        return JsonResponse({"timestamp": timestamp.strftime('%B %d, %Y, %I:%M %p'), "user": request.user.username})
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def revert(request, id):
    if request.method == "POST":
        edit = Edit.objects.get(pk=id)
        article = edit.article
        article.content = edit.content
        article.edit_timestamp = datetime.now()
        article.save()
        revert_edit = Edit(article=article, user=request.user, title=f"Revert to edit #{id}", content=edit.content, timestamp = datetime.now(), status=1, approving_user=request.user)
        revert_edit.save()
        return HttpResponseRedirect(reverse("index"))
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def revert_original(request, title):
    if request.method == "POST":
        article = Article.objects.filter(title=title).get()
        original = Original_Article.objects.filter(article=Article.objects.filter(title=title).get()).get()
        article.content = original.content
        article.edit_timestamp = datetime.now()
        article.save()
        revert_edit = Edit(article=article, user=request.user, title=f"Revert to original version", content=original.content, timestamp = datetime.now(), status=1, approving_user=request.user)
        revert_edit.save()
        return HttpResponseRedirect(reverse("index"))
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))