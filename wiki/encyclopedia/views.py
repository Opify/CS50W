from django.shortcuts import render, HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
import markdown
import re
import random
import datetime

# Task 2, 6 (both done)
def index(request):
    entries = util.list_entries()
    random.seed(datetime.datetime.now())
    rand = entries[random.randint(0, len(entries) - 1)]
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "random": rand
    })

# Tasks 1 and 7 (both done)
def article(request, entry):
    if entry in util.list_entries():
        site = markdown.markdown(util.get_entry(entry))
        return render(request, "encyclopedia/article.html", {
            "title": entry,
            "content": site
        })
    else:
        return render(request, "encyclopedia/error.html")
    
# Task 3 (done)
def query(request):
    query = request.GET["q"]
    if query in util.list_entries():
        return article(request, query)
    else:
        suggestions = []
        # use regex to generate list of suggested articles
        for entry in util.list_entries():
            if re.search(query, entry) is not None:
                suggestions.append(entry)
        return render(request, "encyclopedia/query.html", {
            "results": suggestions
        })

# Task 4 (done)
def create(request):
    # handle form creation
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in util.list_entries():
            return index(request)
        if title == None:
            return create(request)
        util.save_entry(title, content)
        return article(request, title)
    # handle getting to form
    else:
        return render(request, "encyclopedia/create.html")
