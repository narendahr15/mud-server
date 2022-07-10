"""
Class to handle the urls for the client.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.room, name="room"),
]
