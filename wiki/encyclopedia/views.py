from django.shortcuts import render
from . import util
import markdown
import re

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
    
# Task 3
def query(request, query):
    if query in util.list_entries():
        return article(request, query)
    else:
        suggestions = []
        # use regex to generate list of suggested articles
        for entry in util.list_entries:
            if re.search(query, entry) is not None:
                suggestions.append(entry)
            return render(request, "encyclopedia/query.html", {
                "results":suggestions
            })