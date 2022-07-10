import pytest
from commands.cmdhandler import GameEvents
from commands.cmdparser import CommandParser


@pytest.mark.parametrize(
    "is_authenticated, expected_result",
    [
        (True, ["north|south|east|west|n|s|e|w", "quit|exit|logout", "help", "look|l", "say"]),
        (False, ["register", "connect", "help"]),
    ],
)
def test_get_available_commands(is_authenticated, expected_result):
    assert CommandParser.get_available_commands(is_authenticated) == expected_result


@pytest.mark.parametrize(
    "command, is_user_authenticated, expected_event, args",
    [
        # Register command
        (
            "register user user",
            False,
            GameEvents.REGISTER_VALID,
            {"username": "user", "password": "user"},
        ),
        # Connect command
        (
            "connect user user",
            False,
            GameEvents.LOGIN_VALID_PARAM,
            {"username": "user", "password": "user"},
        ),
        # Logout command
        ("quit", True, GameEvents.LOGOUT_VALID, {}),
        ("exit", True, GameEvents.LOGOUT_VALID, {}),
        ("logout", True, GameEvents.LOGOUT_VALID, {}),
        # Help command
        ("help", True, GameEvents.HELP_VALID, {}),
        # Look command
        ("look", True, GameEvents.LOOK_VALID, {}),
        # Say command
        ("say hello Jim", True, GameEvents.SAY_VALID, {"message": "hello Jim"}),
        # Move command
        ("north", True, GameEvents.MOVE_VALID, {"direction": "north"}),
        ("south", True, GameEvents.MOVE_VALID, {"direction": "south"}),
        ("east", True, GameEvents.MOVE_VALID, {"direction": "east"}),
        ("west", True, GameEvents.MOVE_VALID, {"direction": "west"}),
        ("s", True, GameEvents.MOVE_VALID, {"direction": "south"}),
        ("e", True, GameEvents.MOVE_VALID, {"direction": "east"}),
        ("w", True, GameEvents.MOVE_VALID, {"direction": "west"}),
        ("n", True, GameEvents.MOVE_VALID, {"direction": "north"}),
    ],
)
def test_parse_command(command, is_user_authenticated, expected_event, args):
    assert CommandParser.parse_command(command, is_user_authenticated) == (expected_event, args)


@pytest.mark.parametrize(
    "command, is_user_authenticated, expected_event, args",
    [
        # Register command
        (
            "register user",
            False,
            GameEvents.REGISTER_INVALID,
            {},
        ),
        # Connect command
        (
            "connect",
            False,
            GameEvents.LOGIN_INVALID_PARAM,
            {},
        ),
        # Logout command
        ("quit", False, GameEvents.INVALID_COMMAND, {}),
        ("exit", False, GameEvents.INVALID_COMMAND, {}),
        ("logout", False, GameEvents.INVALID_COMMAND, {}),
        # Look command
        ("look", False, GameEvents.INVALID_COMMAND, {}),
        # Say command
        ("say hello Jim", False, GameEvents.INVALID_COMMAND, {}),
    ],
)
def test_parse_invalid_command(command, is_user_authenticated, expected_event, args):
    assert CommandParser.parse_command(command, is_user_authenticated) == (expected_event, args)
