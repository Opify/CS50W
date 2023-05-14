from django.shortcuts import render, HttpResponseRedirect
from . import util
from django import forms
import markdown
import re

class createForm(forms.Form):
    title = forms.TextInput()
    content = forms.Textarea()

# Task 2 (done)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Tasks 1 and 7 (both done)
def article(request, entry):
    if entry in util.list_entries():
        site = markdown.markdown(util.get_entry(entry))
        return render(request, "encyclopedia/article.html", {
            "title":entry,
            "content":site
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
            "results":suggestions
        })

# Task 4
def create(request):
    # handle form creation
    if request.method == "POST":
        form = createForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data.get("Title")
            data = form.cleaned_data.get("Content")
            if filename in util.list_entries():
                return index(request)
            else:
                util.save_entry(filename, data)
                return article(request, filename)
    # handle getting to form
    else:
        return render(request, "encyclopedia/create.html", {
            "form":createForm()
        })
