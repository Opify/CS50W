from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("all_pages", views.all_pages, name="all_pages"),
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
    path("random", views.random_article, name="random"),
    path("follow/<int:id>", views.follow_article, name="follow"),
    path("following", views.following, name="following"),
    path("query", views.query, name="query"),
    path("revert/<int:id>", views.revert, name="revert"),
    path("revert_original/<str:title>", views.revert_original, name="revert_original"),
    path("groups", views.group_index, name="groups"),
    path("group/<str:group>", views.group, name="group"),
    path("pending", views.approve_index, name="approve_index"),
    path("pending/<str:title>", views.approve_view, name="approve"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("edit_profile/<str:user>", views.edit_profile, name="edit_profile"),
    path("follow_user/<str:user>", views.check_follow_user, name="check_follow_user")
    ]