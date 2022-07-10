"""
Class for handling the commands supported by the server.

Each command class is derived from the Command class. Each command class should have a key parameter that is a list
of commands supported by the command. The key parameter is used to determine if the command is supported by the command.

Users can extend the command class by adding their own commands to the command class.
"""
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class GameEvents:
    """
    Events that can be triggered by the game.

    Command handlers can listen for these events and act accordingly. For now, the events are returned
    as strings. No event trigerring is implemented yet.

    Each event has a name and a description. The description is used to describe the event to the user.

    Note: Instead of returning events for failed commands, raise exceptions instead.
    TODO : Implement event triggering.
    TODO : Raise exceptions for failed commands.
    """

    # REGISTER EVENTS
    REGISTER_VALID = "register_event"
    REGISTER_INVALID = "register_invalid_event"
    # LOGIN EVENTS
    LOGIN_VALID_PARAM = "login_success"
    LOGIN_INVALID_PARAM = "login_invalid_param"
    # LOGOUT EVENTS
    LOGOUT_VALID = "logout_success"
    # ROOM EVENTS
    MOVE_VALID = "move_success"
    # LOOK EVENTS
    LOOK_VALID = "look_success"
    # SAY EVENTS
    SAY_VALID = "say_success"
    SAY_INVALID = "say_invalid_param"
    # HELP EVENTS
    HELP_VALID = "help_success"
    # INVALID EVENTS
    INVALID_COMMAND = "invalid_command"


# TODO : Defensive programming
# Now, we have to make sure that the command handler's parse is not called with invalid parameters.
# We assume the caller validated the command by calling the is_command method before calling the parse method.
# We have to make sure that the command handler parse is not called with invalid parameters


class Command(ABC):
    """
    Base class for all commands.

    Each command has a key, which is a list of strings that represent the command. Each command has a
    parser method that is called when the command is received. The parser method should return a tuple
    containing the event name and the arguments for the event.

    The parser method should be implemented by each command.

    Attributes:
        key: A list of strings that represent the command.
    """

    key: list = []

    def is_command(self, command: str) -> bool:
        """
        Checks if the command is a valid command.

        Args:
            command: The command to check.

        Returns:
            True if the command is a valid command, False otherwise.
        """
        logger.debug(f"{self.__class__.__name__} == {self.__class__.key}")
        return command in self.key

    @abstractmethod
    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
        """
        pass

    def __str__(self) -> str:
        """String representation of the command.

        Returns:
            str: The string representation of the command.
        """
        return "|".join(self.__class__.key)


class RegisterCommand(Command):
    """
    Class to validate and parse the command for registering a new user.

    Attributes:
        key: A list of strings that represent the register command.
    """

    key = ["register"]

    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.REGISTER_VALID, {'username': 'username', 'password': 'password'})
        """
        logger.debug(f"RegisterCommand parse: {command}")
        # Slicing to ignore the command key
        command = command[1:]
        if len(command) == 2:
            logger.debug(f"RegisterCommand parsed: {command}")
            return GameEvents.REGISTER_VALID, {"username": command[0], "password": command[1]}
        else:
            logger.debug(f"RegisterCommand invalid: {command}")
            return GameEvents.REGISTER_INVALID, {}


class ConnectCommand(Command):
    """
    Class to validate and parse the command for connecting a registered user.

    Attributes:
        key: A list of strings that represent the connect command.
    """

    key = ["connect"]

    def parse(self, command):
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.LOGIN_VALID_PARAM, {'username': 'username', 'password': 'password'})
        """
        # Slicing to ignore the command key
        command = command[1:]
        if len(command) == 2:
            logger.debug(f"ConnectCommand parsed: {command}")
            return GameEvents.LOGIN_VALID_PARAM, {"username": command[0], "password": command[1]}
        else:
            logger.debug(f"RegisterCommand invalid : {command}")
            return GameEvents.LOGIN_INVALID_PARAM, {}


class LogoutCommand(Command):
    """
    Class to validate and parse the command for logging out a user.

    Attributes:
        key: A list of strings that represent the logout command.
    """

    key = ["quit", "exit", "logout"]

    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.LOGOUT_VALID, {})
        """
        return GameEvents.LOGOUT_VALID, {}


class DirectionCommand(Command):
    """
    Class to validate and parse the command for moving in a direction.

    Attributes:
        key: A list of strings that represent the direction command.
    """

    key = ["north", "south", "east", "west", "n", "s", "e", "w"]

    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.MOVE_VALID, {'direction': 'direction'})
        """
        direction_map = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
        }
        direction = command[0]
        # Convert the short case to long case
        if direction in direction_map:
            logger.debug("DirectionCommand short form converted to long form")
            direction = direction_map[direction]

        logger.debug(f"DirectionCommand parsed: {direction}")
        # TODO : Direction with additional parameters are also supported
        # e.g. north 1 is valid
        return GameEvents.MOVE_VALID, {"direction": direction}


class LookCommand(Command):
    """
    Class to validate and parse the command for looking at a location.

    Attributes:
        key: A list of strings that represent the look command.
    """

    key = ["look", "l"]

    def parse(self, command: str) -> tuple:
        return GameEvents.LOOK_VALID, {}


class SayCommand(Command):
    """
    Class to validate and parse the command for speaking to a character.

    Attributes:
        key: A list of strings that represent the say command.
    """

    key = ["say"]

    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.SAY_VALID, {'message': 'message'})
        """
        return GameEvents.SAY_VALID, {"message": " ".join(command[1:])}


class HelpCommand(Command):
    """
    Class to validate and parse the command for displaying the help menu.

    Attributes:
        key: A list of strings that represent the help command.
    """

    key = ["help"]

    def parse(self, command: str) -> tuple:
        """
        Parses the command and returns the event name and the arguments for the event.

        Args:
            command: The command to check.

        Returns:
            A tuple containing the event name and the arguments for the event.
            e.g (GameEvents.HELP_VALID, {})
        """
        return GameEvents.HELP_VALID, {}
