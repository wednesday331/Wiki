from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.entry, name="entrypage"),
    path("wiki/<str:entryname>/edit", views.edit, name="edit"),
    path("newentrypage", views.newentry, name="newentrypage"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]
