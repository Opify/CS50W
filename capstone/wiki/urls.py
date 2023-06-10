from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("wiki/<str:title>", views.article, name="article"),
    path("edits/<str:title>", views.edits, name="edits")
    ]