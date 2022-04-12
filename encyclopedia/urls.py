from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    # path("<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("editEntry", views.editEntry, name="editEntry"),
    path("randomEntry", views.randomEntry, name="randomEntry"),
    path("<str:title>", views.entry, name="entry")
    
   
    # path("edit/<str:title>", views.editEntry, name="editEntry")
    
    
]
