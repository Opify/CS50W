from django.shortcuts import render, HttpResponse
from . import util
import markdown

# Task 2
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Task 1, 7 (both done)
def entry(request, article):
    site = util.get_entry(article)
    if site is None:
        return render(request, "encyclopedia/error.html")
    else:
        site = markdown.markdown(site)
        return render(request, "encyclopedia/article.html", {
            "title": article,
            "content": site
        })

