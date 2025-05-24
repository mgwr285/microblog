from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("explore/", views.explore, name="explore"),
    path("<str:username>/", views.user, name="user"),
]
