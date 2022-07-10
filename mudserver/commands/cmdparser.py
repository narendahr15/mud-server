"""
Class for parsing commands.

This class determines what commands are available to the user and parse them.

This class has to be modified to support new commands.
"""
import logging

import commands.cmdhandler as cmd

logger = logging.getLogger(__name__)


class CommandParser:
    """
    Command parser class.

    Responsible for parsing commands and returning the event name and the arguments for the event.
    Also responsible for providing the selected command list based on whether the user is logged in or not.

    Attributes:
        commands: A list of commands.
    """

    # Commands that are available to the user when they are not logged in.
    anonymous_user_commands = [cmd.RegisterCommand(), cmd.ConnectCommand(), cmd.HelpCommand()]
    # Commands that are available to the user when they are logged in.
    authenticated_user_commands = [
        cmd.DirectionCommand(),
        cmd.LogoutCommand(),
        cmd.HelpCommand(),
        cmd.LookCommand(),
        cmd.SayCommand(),
    ]

    @staticmethod
    def parse_command(command, is_user_authenticated: bool) -> tuple:
        """
        Parses a command string into a list of arguments.

        Args:
            command: The command string to parse.
            is_user_authenticated: Whether the user is authenticated or not.

        Returns:
            A tuple containing the event name and the arguments for the event.
        """
        command = command.split(" ")
        command_key = command[0].lower()
        command_set = (
            CommandParser.anonymous_user_commands
            if not is_user_authenticated
            else CommandParser.authenticated_user_commands
        )
        for command_class in command_set:
            if command_class.is_command(command_key):
                logger.debug(f"{command_class.__class__.__name__} matches parse_command: {command}")
                return command_class.parse(command)

        return cmd.GameEvents.INVALID_COMMAND, {}

    @staticmethod
    def get_available_commands(is_user_authenticated: bool) -> list:
        """Get a list of available commands based on whether the user is authenticated or not

        Args:
            is_user_authenticated (bool): Whether the user is authenticated or not.

        Returns:
            list: A list of available commands.
        """
        command_set = (
            CommandParser.anonymous_user_commands
            if not is_user_authenticated
            else CommandParser.authenticated_user_commands
        )
        logger.debug(f"Available commands: {command_set}")
        return [str(command_class) for command_class in command_set]
