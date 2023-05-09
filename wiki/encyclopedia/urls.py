from django.urls import path

from . import views

# for app
urlpatterns = [
    path("", views.index, name="index")
]
