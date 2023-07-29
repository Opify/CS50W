from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.post, name="post"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("edits/<str:title>", views.edits, name="edits"),
    path("view_edit/<int:id>", views.edit_view, name="edit_view"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("random", views.random_post, name="random"),
    path("following", views.following, name="following"),
    path("query", views.query, name="query"),
    path("groups", views.group_index, name="groups"),
    path("group/<str:group>", views.group, name="group"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("edit_profile/<str:user>", views.edit_profile, name="edit_profile"),
    path("follow_user/<str:user>", views.check_follow_user, name="check_follow_user")
    ]