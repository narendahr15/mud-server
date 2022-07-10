"""
Class to handle the views for the client.
"""
from django.shortcuts import render


def index(request):
    return render(request, "client/index.html")


def room(request):
    return render(request, "client/room.html")
