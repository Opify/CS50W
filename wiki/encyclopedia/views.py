from django.shortcuts import render, HttpResponse
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, article):
    site = util.get_entry(article)
    if site is None:
        return render(request, "encyclopedia/error.html")
    else:
        return HttpResponse(markdown2.markdown(site))

