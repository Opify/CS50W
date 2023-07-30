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


def index(request):
    try:
        day_post = random.choice(Post.objects.all())
    except:
        return HttpResponseRedirect(reverse('all_posts'))
    try:
        comments = Comment.objects.filter(post=day_post).order_by('-timestamp').all()
    except:
        comments = None
    try:
        groups = Group.objects.filter(post=day_post).all()
    except:
        groups = None
    try:
        background_colour = day_post.user.background_color
    except:
        background_colour = None
    try:
        text_colour = day_post.user.text_color
    except:
        text_colour = None
    content = markdown.markdown(day_post.content)
    return render(request, "blog/index.html", {
        "post": day_post,
        "content": content,
        "comments": comments,
        "groups": groups,
        "background_colour": background_colour,
        "text_colour": text_colour
    })

def all_posts(request):
    try:
        posts = Post.objects.order_by('-create_timestamp').all()
    except:
        posts = None
    return render(request, "blog/all_pages.html", {
        "posts": posts
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
            return render(request, "blog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "blog/login.html")

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
            return render(request, "blog/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "blog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blog/register.html")

# handle rendering of profile page and following user
def profile(request, user):
    if request.method == "POST":
        try:
            following = Following.objects.filter(following=User.objects.get(username=user), follower=request.user).get()
        except:
            following = Following(following=User.objects.get(username=user), follower=request.user)
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
                interests = Group.objects.filter(interested=profile_info).all()
            except:
                interests = None
            try:
                posts_created = Post.objects.filter(user=profile_info).all()
                posts = []
                for post in posts_created:
                    posts.append(post.title)
            except:
                posts = None
            try:
                following = Following.objects.filter(following=User.objects.filter(username=user).get(), follower=request.user).get()
            except:
                following = None
            try:
                background_colour = profile_info.background_color
            except:
                background_colour = None
            try:
                text_colour = profile_info.text_color
            except:
                text_colour = None
            if following:
                following = "Unfollow"
            else:
                following = "Follow"
            return render(request, "blog/profile.html", {
                "profile": profile_info,
                "interests": interests,
                "posts": posts,
                "following": following,
                "background_colour": background_colour,
                "text_colour": text_colour
            })

@login_required
def edit_profile(request, user):
    if request.method == "POST":
        bio = request.POST["bio"]
        new_interests = request.POST["group"]
        background_colour = request.POST["background_colour"]
        text_colour = request.POST["text_colour"]
        profile = User.objects.filter(username=user).get()
        profile.bio = bio
        if background_colour != "":
            profile.background_color = background_colour
        else:
            profile.background_color = None
        if text_colour != "":
            profile.text_color = text_colour
        else:
            profile.text_color = None
        profile.save()
        if new_interests == "":
            try:
                current_interests = Group.objects.filter(interested=request.user).all()
            except:
                pass
            else:
                current_interests.delete()
        else:
            interests = new_interests.split(", ")
            try:
                current_interests = Group.objects.filter(interested=request.user).all()
            except:
                current_interests.delete()
            for interest in interests:
                capitalised = interest.capitalize()
                new_interest = Group(interested=request.user, group=capitalised)
                new_interest.save()
        return HttpResponseRedirect(reverse('profile', args=[user]))
    else:
        try:
            profile = User.objects.filter(username=user).get()
        except:
            return HttpResponseRedirect(reverse('index'))
        try:
            interest = Group.objects.filter(interested=request.user).values_list('group', flat=True)
            interest = ", ".join(interest)
        except:
            interest = None
        try:
            background_colour = profile.background_color
        except:
            background_colour = None
        try:
            text_colour = profile.text_color
        except:
            text_colour = None
        return render(request, "blog/edit_profile.html", {
            "profile": profile,
            "interest": interest,
            "background_colour": background_colour,
            "text_colour": text_colour
        })

@login_required
def create(request):
    # handle post creation
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        groups = request.POST.get("group")
        # checks if post already exists via title
        try:
            Post.objects.filter(title=title).get()
        except:
            post = Post(user=request.user, title=title, content=content, create_timestamp=datetime.now())
            post.save()
            if groups != "":
                groups.split(", ")
                for group in groups:
                    capitalised = group.capitalize()
                    grouping = Group(post=post, group=capitalised)
                    grouping.save()
            return HttpResponseRedirect(reverse("post", args=[title]))
        else:
            return HttpResponseRedirect(reverse("index"))
    # handle getting to form
    else:
        return render(request, "blog/create.html")

# Display post and coments
def post(request, title):
    try:
        post = Post.objects.filter(title=title).get()
    except:
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            comments = Comment.objects.filter(post=post).order_by('-timestamp').all()
        except:
            comments = None
        try:
            groups = Group.objects.filter(post=post).all()
        except:
            groups = None
        titles = list(Post.objects.filter(user=post.user).order_by('-create_timestamp').values_list('title', flat=True))
        if len(titles) > 1:
            if title == titles[0]:
                first = None
                previous = titles[1]
                next = None
                last = titles[-1]
            elif title == titles[-1]:
                first = titles[0]
                previous = None
                next = titles[-2]
                last = None
            elif len(titles) > 2:
                first = titles[0]
                previous = titles[titles.index(title) + 1]
                next = titles[titles.index(title) - 1]
                last = titles[-1]
        else:
            previous = None
            next = None
        content = markdown.markdown(post.content)
        try:
            background_colour = post.user.background_color
        except:
            background_colour = None
        try:
            text_colour = post.user.text_color
        except:
            text_colour = None
        return render(request, "blog/post.html", {
            "post": post,
            "content": content,
            "comments": comments,
            "groups": groups,
            "first": first,
            "previous": previous,
            "next": next,
            "last": last,
            "background_colour": background_colour,
            "text_colour": text_colour
        })

# Display random post
def random_post(request):
    try:
        posts = Post.objects.values_list('title', flat=True)
        return HttpResponseRedirect(reverse("post", args=[random.choice(posts)]))
    except:
        return HttpResponseRedirect(reverse("index"))

# Display lists of edits for an post
def edits(request, title):
    try:
        post = Post.objects.filter(title=title).get()
        edits = Edit.objects.filter(post=post).order_by('-timestamp').all()
    except:
        return HttpResponseRedirect(reverse("post", args=[title]))
    else:
        changes = []
        for edit in edits:
            list = []
            list.append(edit)
            list.append(util.track_changes(edit.old_content, edit.new_content))
            changes.append(list)
        # if you're wondering how each change is stored, index 0 is the edit itself, index 1 is the list used to display changes made
        return render(request, "blog/edits.html", {
            "changes": changes,
            "title": title
        })

@login_required
# handle edits
def edit(request, title):
    # handle edit logic
    if request.method == "POST":
        try:
            post = Post.objects.filter(title=title).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            group = request.POST.get("group")
            content = request.POST.get("content")
            if group != "":
                try:
                    original_groups = Group.objects.filter(post=post).all()
                except:
                    pass
                else:
                    original_groups.delete()
                groups = group.split(", ")
                for value in groups:
                    capitalised = value.capitalize()
                    new_group = Group(post=post, group=capitalised)
                    new_group.save()
                edit = Edit(post=post, user=request.user, old_content=post.content, new_content=content, timestamp=datetime.now(), groups=", ".join(groups))
                edit.save()
            else:
                try:
                    original_groups = Group.objects.filter(post=post).all()
                except:
                    pass
                else:
                    original_groups.delete()
                edit = Edit(post=post, user=request.user, old_content=post.content, new_content=content, timestamp=datetime.now())
                edit.save()
            post.content = content
            post.edit_timestamp = datetime.now()
            post.save()
            return HttpResponseRedirect(reverse("post", args=[title]))
    # handle edit page
    else:
        try:
            post = Post.objects.filter(title=title).get()
        except:
            return HttpResponseRedirect(reverse("index"))
        else:
            try:
                groups = Group.objects.filter(post=post).values_list('group', flat=True)
                groups = ", ".join(groups)
            except:
                groups = None
            return render(request, "blog/edit.html", {
                "post": post,
                "groups": groups
            })

# Display view edits
def edit_view(request, id):
    try:
        edit = Edit.objects.get(pk=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    else:
        post = edit.post
        content = markdown.markdown(edit.new_content)
        return render(request, "blog/edit_view.html", {
            "edit": edit,
            "content": content,
            "post": post
        })

# handle following page and getting to following
@login_required
def following(request):
    # handle following page
    if request.method == "GET":
        try:
            following_users = Following.objects.filter(follower=request.user).all()
        except:
            following_users = None
        return render(request, "blog/following.html", {
            "following_users": following_users
        })
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required
def check_follow_user(request, user):
    try:
        following = Following.objects.filter(following=User.objects.filter(username=user).get(), follower=request.user).get()
    except:
        return JsonResponse({"followed": "false"})
    else:
        return JsonResponse({"followed": "true"})

# handle query results
def query(request):
    query = request.GET["q"]
    posts = Post.objects.values_list('title', flat=True)
    if query in posts:
        return HttpResponseRedirect(reverse("post", args=[query]))
    else:
        suggestions = []
        # use regex to generate list of suggested posts
        for post in posts:
            if re.search(query, post) is not None:
                suggestions.append(post)
        return render(request, "blog/query.html", {
            "results": suggestions
        })

@login_required    
# handle uploading comments from posts
def comment(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        content = body.get("comment")
        timestamp = datetime.now()
        user = request.user
        comment = Comment(post=Post.objects.get(pk=id), user=user, comment=content, timestamp=timestamp)
        comment.save()
        return JsonResponse({"timestamp": timestamp.strftime('%B %d, %Y, %I:%M %p'), "user": request.user.username})
    # reject all other methods
    else:
        return HttpResponseRedirect(reverse("index"))

# Display lists of groups
def group_index(request):
    raw = Group.objects.values_list("group", flat=True)
    # get unique groups
    groups = set(raw)
    return render(request, "blog/groups.html", {
        "groups": groups
    })

# Display interests and posts in a group
def group(request, group):
    try:
        entries = Group.objects.filter(group=group).all()
    except:
        return HttpResponseRedirect(reverse(index))
    interested = []
    posts = []
    for entry in entries:
        # if interest is null, it must be an post
        if not entry.interested:
            posts.append(entry)
        # if post is null, it must be an interest
        elif not entry.post:
            interested.append(entry)
    return render(request, "blog/group.html", {
        "interested": interested,
        "posts": posts,
        "group": group
    })