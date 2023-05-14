from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("query/q<str:query>", views.query, name="query"),
    path("<slug:entry>", views.article, name="article")
]
