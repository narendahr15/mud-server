"""
Class to handle the map of the game.

Also supports in navigation of the map.
"""
import logging
from dataclasses import dataclass

from .data import room_data

logger = logging.getLogger(__name__)

# Default room
DEFAULT_ROOM_INDEX = 0


# TODO : Map the rooms to the ORM model so that we can add rooms to the database dynamically.
# TODO Validate the JSON data describing the rooms and the exits


@dataclass(frozen=True)
class Exit:
    """
    Class to represent an exit.

    Attributes:
        name: The name of the exit.
        id: The id of the exit.
        location: The id of the room where the exit is.
        destination: The id of the room where the exit leads to.
    """

    id: int
    name: str
    location: int
    destination: int


@dataclass(frozen=True)
class Room:
    """
    Class to represent a room.

    Attributes:
        id: The id of the room.
        name: The name of the room.
        description: The description of the room.
        exits: A list of exits in the room.
    """

    id: int
    name: str
    desc: str
    exits: list


def construct_rooms(room_data: dict) -> list:
    """
    Constructs a list of rooms from the data in the room_data dict.

    Args:
        room_data: A dict containing the data for the rooms.

    Returns:
        A list of rooms.
    """
    rooms = []
    for room_dict in room_data["rooms"]:
        room_id = room_dict["id"]
        logger.debug(f"Constructing room {room_id}")
        exits = []

        # Create the exits for the room
        # TODO: Check for multiple exits in the same direction
        # This is a bit of a hack. This logic allows a room to have exits
        # to the different rooms for the same direction. The get_room_by_id()
        # will fetch the first exit in the list of exits for the room.
        for exit_dict in room_data["exits"]:
            if exit_dict["location"] == room_id:
                logger.debug(f"Adding exit {exit_dict['id']} to room {room_id}")
                exit = Exit(**exit_dict)
                exits.append(exit)

        room_dict["exits"] = exits
        room = Room(**room_dict)
        rooms.append(room)
        logger.debug(f"Constructed room {room_id}")
    return rooms


rooms = construct_rooms(room_data)


class MapNavigator:
    """
    Class to help navigating the map.
    """

    @staticmethod
    def get_default_room_id():
        """
        Gets the default room id.

        Returns:
            int: The default room id.
        """
        # Assumptions : There is always a default room and it is the first room in the list.
        return rooms[DEFAULT_ROOM_INDEX].id

    @staticmethod
    def get_room(room_id: int) -> Room:
        """Gets the room with the given id.

        Args:
            room_id (int): Room id.

        Returns:
            Room: Room with the given id.
        """
        logging.debug(f"Getting room with id {room_id}")
        for room in rooms:
            if room.id == room_id:
                return room
        return None

    @staticmethod
    def move_to(current_location_id: int, direction: str) -> int:
        """
        Moves to the room in the given direction.

        Args:
            current_location_id (int): The id of the current room.
            direction (str): The direction to move.

        Returns:
            int: The id of the room that the player is moved to.
        """
        # Get the room that the player is in
        logger.debug(f"Moving {direction} from {current_location_id}")
        current_location = [room for room in rooms if room.id == current_location_id][0]
        logger.debug("Current location: " + str(current_location))

        # Check if the direction is valid
        for exit in current_location.exits:
            logger.debug("Exit: " + str(exit))
            if exit.name == direction:
                logger.debug("Found exit: " + str(exit))
                return exit.destination
        logger.error("No exit found")

        # If no exit was found, return the current location
        return current_location_id

    @staticmethod
    def get_room_name(room_id: int) -> str:
        """Get the name of the room with the given id.

        Args:
            room_id (int): Room id.

        Returns:
            str: The name of the room.
        """
        room = MapNavigator.get_room(room_id)
        if room:
            return room.name
        return None

    @staticmethod
    def get_printable_exits(room: Room) -> list:
        """
        Gets the printable exits for the given room.

        Args:
            room (Room): The room to get the exits for.

        Returns:
            list(str): The printable exits for the room.
        """
        exits = []
        for exit in room.exits:
            destination_name = MapNavigator.get_room_name(exit.destination)
            exits.append(f"{destination_name}#({exit.name})")
        return exits
