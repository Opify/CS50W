from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.article, name="article"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("edits/<str:title>", views.edits, name="edits"),
    path("view_edit/<int:id>", views.edit_view, name="edit_view"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("edit_comment/<int:id>", views.edit_comment, name="edit_comment"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("query", views.query, name="query"),
    path("revert/<int:id>", views.revert, name="revert"),
    path("revert_original/<str:title>", views.revert_original, name="revert_original")
    ]