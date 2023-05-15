from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("query", views.query, name="query"),
    path("edit", views.edit, name="edit"),
    path("<slug:entry>", views.article, name="article")
]
