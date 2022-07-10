"""
File to model the game profiles.

Users can create new profiles and save them to the database.
"""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Base class for all profiles

    Users can extend the profile class to add additional profiles.
    e.g PlayerProfile, WeaponProfile, etc.

    Attributes:
        location: The location of the user.
    """

    location = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PlayerProfile(Profile):
    """
    Player profile class. Matches the Player model in the database.
    Has a one-to-one relationship with the User model.

    Attributes:
        user: The user that this profile belongs to.
        is_connected: Whether the player is currently connected to the server.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_connected = models.BooleanField(default=False)
