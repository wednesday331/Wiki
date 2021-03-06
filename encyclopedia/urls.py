from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryname>", views.entry, name="entry_page"),
    path("wiki/<str:entryname>/edit", views.edit, name="edit"),
    path("newentrypage", views.new_entry, name="new_entry_page"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]
