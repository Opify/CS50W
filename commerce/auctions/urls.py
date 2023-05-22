from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("<int:id>", views.listing, name="listing"),
    path("close/<int:id>", views.close, name="close")
]
