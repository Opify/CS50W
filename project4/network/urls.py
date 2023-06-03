
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("following", views.following, name="following"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like"),
    path("check_like/<int:id>", views.check_like, name="check_like")
]
