from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<slug:category>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("<int:id>", views.listing, name="listing"),
    path("close/<int:id>", views.close, name="close")
]
