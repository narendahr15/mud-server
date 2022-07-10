"""
File containing the routing logic for the client.

"""
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/client/$", consumers.AsyncWebConsumer.as_asgi()),
]
