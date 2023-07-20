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
import random

from . import util
from .models import *


# Display all articles
def all_pages(request):
    articles = Article.objects.filter(status=1).order_by('-create_timestamp').all()
    return render(request, "wiki/all_pages.html", {
        "articles": articles
    })

def index(request):
    try:
        day_article = random.choice(Article.objects.filter(status=1).all())
    except:
        return HttpResponseRedirect(reverse('all_pages'))
    try:
        comments = Comment.objects.filter(article=day_article).order_by('-timestamp').all()
    except:
        comments = None
    try:
        group = Group.objects.filter(article=day_article).get()
    except:
        group = None
    content = markdown.markdown(day_article.content)
    return render(request, "wiki/index.html", {
        "article": day_article,
        "content": content,
        "comments": comments,
        "group": group
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

# handle rendering of profile page and following user
def profile(request, user):
    if request.method == "POST":
        try:
            following = Following_User.objects.filter(following=User.objects.get(username=user), follower=request.user).get()
        except:
            following = Following_User(following=User.objects.get(username=user), follower=request.user)
            following.save()
            return HttpResponse(200)
        else:
            following.delete()
            return HttpResponse(200)
    else:
        try:
            profile_info = User.objects.filter(username=user).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            try:
                expert = Group.objects.filter(expert=profile_info).get()
            except:
                expert = None
            try:
                articles_created = Article.objects.filter(user=profile_info, status=1).all()
                articles = []
                for article in articles_created:
                    articles.append(article.title)
            except:
                articles = None
            try:
                following = Following_User.objects.filter(following=User.objects.filter(username=user).get(), follower=request.user)
            except:
                following = None
            if following:
                following = "Unfollow"
            else:
                following = "Follow"
            return render(request, "wiki/profile.html", {
                "profile": profile_info,
                "expert": expert,
                "articles": articles,
                "following": following
            })

@login_required
def edit_profile(request, user):
    if request.method == "POST":
        bio = request.POST["bio"]
        new_expert = request.POST["group"]
        if new_expert == "":
            try:
                current_expert = Group.objects.filter(expert=request.user).get()
            except:
                pass
            else:
                current_expert.delete()
        else:
            try:
                current_expert = Group.objects.filter(expert=request.user).get()
            except:
                capitalised = new_expert.capitalize()
                updated_expert = Group(expert=request.user, group=capitalised)
                updated_expert.save()
            else:
                capitalised = new_expert.capitalize()
                current_expert.group = capitalised
                current_expert.save()
        profile = User.objects.filter(username=user).get()
        profile.bio = bio
        profile.save()
        return HttpResponseRedirect(reverse('profile', args=[user]))
    else:
        try:
            profile = User.objects.filter(username=user).get()
        except:
            return HttpResponseRedirect(reverse('index'))
        try:
            expert = Group.objects.filter(expert=request.user).get()
        except:
            expert = None
        return render(request, "wiki/edit_profile.html", {
            "profile": profile,
            "expert": expert
        })

@login_required
def create(request):
    # handle article creation
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        group = request.POST.get("group")
        # checks if article already exists via title
        try:
            Article.objects.filter(title=title).get()
        except:
            if group != "":
                capitalised = group.capitalize()
                article = Article(user=request.user, title=title, content=content, create_timestamp=datetime.now(), status=0)
                article.save()
                grouping = Group(article=article, group=capitalised)
                grouping.save()
            else:
                article = Article(user=request.user, title=title, content=content, create_timestamp=datetime.now(), status=0)
                article.save()
            original = Original_Article(article=Article.objects.filter(title=title).get(), content=content)
            original.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))
    # handle getting to form
    else:
        return render(request, "wiki/create.html")

# Display all articles created, either by everyone or by user
@login_required
def approve_index(request):
    if request.user.is_superuser:
        # admins should be able to see all articles
        try:
            pending = Article.objects.order_by('-create_timestamp').all()
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        # users should only be able to see articles they created
        try:
            pending = Article.objects.filter(user=request.user).order_by('-create_timestamp').all()
        except:
            return HttpResponseRedirect(reverse("index"))
    return render(request, "wiki/approval_index.html", {
        "pending": pending
    })

# Handle proposed article contents and approval of articles
def approve_view(request, title):
    if request.method == "POST":
        body = json.loads(request.body)
        action = body.get("action")
        article = Article.objects.get(title=title)
        if action == "accept":
            article.status = 1
            article.save()
            return HttpResponse(200)
        elif action == "reject":
            article.status = 2
            article.save()
            return HttpResponse(200)
        return HttpResponseRedirect(reverse('approve_view', args=[title]))
    else:
        try:
            article = Article.objects.filter(title=title).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            content = markdown.markdown(article.content)
            return render(request, "wiki/approval_view.html", {
                "article": article,
                "content": content
            })

# Display article and coments
def article(request, title):
    try:
        article = Article.objects.filter(title=title, status=1).get()
    except:
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            comments = Comment.objects.filter(article=article).order_by('-timestamp').all()
        except:
            comments = None
        try:
            group = Group.objects.filter(article=article).get()
        except:
            group = None
        content = markdown.markdown(article.content)
        return render(request, "wiki/article.html", {
            "article": article,
            "content": content,
            "comments": comments,
            "group": group
        })

# Display random article
def random_article(request):
    articles = Article.objects.filter(status=1).values_list('title', flat=True)
    return HttpResponseRedirect(reverse("article", args=[random.choice(articles)]))

# Display lists of edits for an article
def edits(request, title):
    try:
        article = Article.objects.filter(title=title, status=1).get()
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
            article = Article.objects.filter(title=title, status=1).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            group = request.POST.get("group")
            if group != "":
                capitalised = group.capitalize()
                edit = Edit(article=article, user=request.user, title=request.POST.get("title"), content=request.POST.get("content"), timestamp=datetime.now(), status = 0, group=capitalised)
            else:
                edit = Edit(article=article, user=request.user, title=request.POST.get("title"), content=request.POST.get("content"), timestamp=datetime.now(), status = 0)
            edit.save()
            return HttpResponseRedirect(reverse("article", args=[title]))
    # handle edit page
    else:
        try:
            article = Article.objects.filter(title=title, status=1).get()
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
            try:
                grouping = Group.objects.filter(article=article).get()
            except:
                if edit.group != "":
                    new_grouping = Group(article=article, group=edit.group)
                    new_grouping.save()
            else:
                if edit.group != grouping.group:
                    if edit.group == "":
                        grouping.delete()
                    else:
                        grouping.group = edit.group
                        grouping.save()
            edit.save()
            article.save()
            return HttpResponse(200)
        elif action == "reject":
            edit.status = 2
            edit.approving_user = request.user
            edit.save()
            return HttpResponse(200)
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
            if current_version != edit and edit.status == 1:
                current = False
            else:
                current = True
            article = edit.article
            content = markdown.markdown(edit.content)
            return render(request, "wiki/edit_view.html", {
                "edit": edit,
                "content": content,
                "edit_comments": edit_comments,
                "current": current,
                "article": article
            })

# handle following page and getting to following
@login_required
def following(request):
    # handle following page
    if request.method == "GET":
        try:
            following_articles = Following_Article.objects.filter(user=request.user).all()
        except:
            following_articles = None
        try:
            following_users = Following_User.objects.filter(follower=request.user).all()
        except:
            following_users = None
        return render(request, "wiki/following.html", {
            "following_articles": following_articles,
            "following_users": following_users
        })
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def follow_article(request, id):
    # handle following article request
    if request.method == "POST":
        try:
            following = Following_Article.objects.filter(article=Article.objects.get(pk=id), user=request.user).get()
        except:
            following = Following_Article(article=Article.objects.get(pk=id), user=request.user)
            following.save()
            return HttpResponse(200)
        else:
            following.delete()
            return HttpResponse(200)
    # check if follow for article exists
    else:
        try:
            following = Following_Article.objects.filter(article=Article.objects.get(pk=id), user=request.user).get()
        except:
            return JsonResponse({"followed": "false"})
        else:
            return JsonResponse({"followed": "true"})

# handle query results
def query(request):
    query = request.GET["q"]
    articles = Article.objects.filter(status=1).values_list('title', flat=True)
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

# Display lists of groups
def group_index(request):
    raw = Group.objects.values_list("group", flat=True)
    # get unique groups
    groups = set(raw)
    return render(request, "wiki/groups.html", {
        "groups": groups
    })

# Display experts and articles in a group
def group(request, group):
    try:
        entries = Group.objects.filter(group=group).all()
    except:
        return HttpResponseRedirect(reverse(index))
    experts = []
    articles = []
    for entry in entries:
        # if expert is null, it must be an article
        if not entry.expert:
            if entry.article.status == 1:
                articles.append(entry)
        # if article is null, it must be an expert
        elif not entry.article:
            experts.append(entry)
    return render(request, "wiki/group.html", {
        "experts": experts,
        "articles": articles,
        "group": group
    })