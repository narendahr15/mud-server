"""
Class to handle the state of the player.

Handles all the events triggered by the player.
"""
import json
import logging

import django.db as django_db
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from channels.auth import login, logout
from channels.db import database_sync_to_async

from commands.cmdparser import CommandParser
from commands.cmdhandler import GameEvents
from game.models import PlayerProfile
from game.rooms.map_navigator import MapNavigator


logger = logging.getLogger(__name__)


class GameEngine:
    groups = ["broadcast"]

    def __init__(self, consumer, channel_layer) -> None:
        """Initialize the game engine

        Args:
            consumer (AsyncWebSocketConsumer): The consumer object
            channel_layer (ChannelLayer): The channel layer object
        """
        logging.debug("GameEngine __init__")
        self.command_handlers = {
            GameEvents.REGISTER_VALID: self.__register_user,
            GameEvents.HELP_VALID: self.__help,
            GameEvents.LOGIN_VALID_PARAM: self.__connect_user,
            GameEvents.LOOK_VALID: self.__look,
            GameEvents.SAY_VALID: self.__say,
            GameEvents.MOVE_VALID: self.__move_to,
            GameEvents.LOGOUT_VALID: self.__quit,
        }

        self.consumer = consumer
        self.channel_layer = channel_layer
        self.__init_state_var()

    def __init_state_var(self):
        """
        Initialize the state variables. The state variables are updated
        whenever the user moves to a new location, or logs in or out.

        The state variables are used to maintain the state of the game.
        We maintain the state internally in the game engine to avoid
        accessing the database for each and every request.

        The state is synced with the db whenever the user moves to a new location
        or
        """
        logger.debug("Initializing state variables")
        self.is_user_authenticated = False
        self.room = None
        self.player = None
        self.username = None

    @database_sync_to_async
    def __create_user(self, name: str, password: str) -> User:
        """
        Create a new user

        Creates a new user from the given name and password.
        Also creates a new player profile for the user.

        Args:
            name (str): The name of the user
            password (str): The password of the user

        Returns:
            User: The user object

        Throws:
            IntegrityError: If the user already exists
        """
        user = User.objects.create_user(username=name, password=password)
        user.save()
        # TODO : Replace creating a player profile with a signal
        player_profile = PlayerProfile.objects.create(
            user=user, is_connected=False, location=MapNavigator.get_default_room_id()
        )
        self.player = player_profile
        player_profile.save()
        return user

    @database_sync_to_async
    def __get_user(self, name: str) -> User:
        """
        Get the user object for the given name

        Args:
            name (str): The name of the user

        Returns:
            User: The user object
        """
        return User.objects.get(username=name)

    @database_sync_to_async
    def __get_player_profile(self, user: User) -> PlayerProfile:
        """
        Gets the player profile for the given user

        Args:
            user (User): The user object

        Returns:
            PlayerProfile: The player profile object
        """
        return PlayerProfile.objects.get(user=user)

    @database_sync_to_async
    def __get_users_in_location(self, location: int) -> list:
        """
        Gets the usernames of all the players in the location

        Args:
            location (int): The location id

        Returns:
            list: The list of usernames
        """
        players = PlayerProfile.objects.filter(location=location, is_connected=True)
        res = []
        for player in players:
            res.append(
                player.user.username,
            )
        return res

    @database_sync_to_async
    def __update_player_status(self, connected: bool) -> None:
        """
        Update the player status

        Args:
            connected (bool): The status of the player (connected or disconnected)
        """
        self.player.is_connected = connected
        self.player.save()

    @database_sync_to_async
    def __update_location(self, location: int) -> None:
        """
        Update the location of the player

        Args:
            location (int): The location id
        """
        self.player.location = location
        self.player.save()

    async def __create(self, name: str, password: str) -> None:
        """
        Create a new user

        Args:
            name (str): The name of the user
            password (str): The password of the user
        """
        user = await self.__create_user(name, password)
        if user:
            await self.__send_message_to_client(
                f"<b>{name}</b> user has been created. Please login using the same credentials."
            )
        else:
            await self.__send_message_to_client(
                "Cannot create user with the given name and password"
            )

    async def __login(self, name: str, password: str) -> User:
        """
        Login the user

        Args:
            name (str): The name of the user
            password (str): The password of the user

        Returns:
            User: The user object

        Throws:
            AuthenticationError: If the user is not authenticated
        """
        # TODO : Current implementation allows multiple login of the same user
        # This results in the user handling the state of the game in multiple sessions
        # Results in conflicts in the game state
        # Need to implement a way to handle the state of the game in a single session
        logger.debug(f"Login request for {name}")
        user = await self.__get_user(name)
        await login(self.consumer.scope, user)
        if user:
            logger.debug("User found..Authenticating..")
            user = await database_sync_to_async(authenticate)(username=name, password=password)
            if user and user.is_authenticated:
                logger.debug("User authenticated..")

                # Set the state variables
                self.player = await self.__get_player_profile(user)
                self.username = user.username
                self.is_user_authenticated = True
                await self.__update_player_status(True)
                logger.debug(f"Location at the time of login :  {self.player.location}")

                # Send the message to the client
                await self.__send_message_to_client("User has been logged in : " + user.username)
                logger.info(f"User {user.username} has logged in")
            else:
                logger.error(f"User <b>{name}<b> failed to login")
                await self.__send_message_to_client("Cannot authenticate user")
        else:
            logger.error(f"User <b>{name}<b> not found")
            await self.__send_message_to_client("Wrong username or password")

        return user if user and user.is_authenticated else None

    async def __register_user(self, username: str, password: str) -> None:
        """
        Register the user

        Args:
            username (str): The name of the user
            password (str): The password of the user
        """
        logger.info("Registering user")
        try:
            await self.__create_new_user(username, password)
        except django_db.utils.IntegrityError:
            await self.__send_message_to_client(
                "Username already taken. Please choose a different username"
            )

    async def __connect_user(self, username: str, password: str) -> None:
        """
        Connect the user to the game

        Args:
            username (str): The name of the user
            password (str): The password of the user
        """
        try:
            user = await self.__login(username, password)
            if user:
                self.room = MapNavigator.get_room(self.player.location)
                await self.__send_message_to_client(
                    f"<b># {self.room.name}<b> <br><br> {self.room.desc}"
                )
                # Broadcast the message to all the users
                await self.channel_layer.group_send(
                    GameEngine.groups[0],
                    {
                        "type": "message.broadcast",
                        "message": f"<b>{self.username}<b> has joined the game",
                    },
                )
        except User.DoesNotExist as e:
            logger.exception(f"User {username} does not exist")
            # Reset the user
            self.__init_state_var()
            await self.__send_message_to_client(
                f"Cannot connect user {username}. Please check the credentials"
            )

    async def __say(self, message: str) -> None:
        """
        Send a message to all the active users in the user's location

        Args:
            message (str): Message to be sent
        """
        await self.channel_layer.group_send(
            GameEngine.groups[0],
            {
                "type": "message.location",
                "location": self.player.location,
                "message": f"<b>{self.username}</b> says <i>{message}<i>",
            },
        )

    async def __move_to(self, direction: str) -> None:
        """
        Move the user to the given direction

        Args:
            direction (str): The direction to move to
        """
        new_location = MapNavigator.move_to(self.player.location, direction)
        await self.__update_location(new_location)
        self.room = MapNavigator.get_room(new_location)
        message = f"""
        <br><b># {self.room.name}<b><br>
        <br>{self.room.desc}
        """
        await self.__send_message_to_client(message)

    async def __look(self):
        """
        Look around the user's location. Displays the description of the roomm,
        players in the room and the exits available
        """
        logger.info(f"Location is: {self.player.location}")
        players = await self.__get_users_in_location(self.player.location)
        players = " ".join(players)
        await self.__send_message_to_client(
            f"""
            <br><b>{self.room.name}</b>
            <br>{self.room.desc}
            <br><b>Players</b>: {players}
            <br><b>Exits</b>: {MapNavigator.get_printable_exits(self.room)}
            """
        )

    async def __quit(self):
        """
        Quits the game/disconnects the user
        """
        await self.channel_layer.group_send(
            GameEngine.groups[0],
            {
                "type": "message.broadcast",
                "message": f"<b>{self.username}<b> has left the game",
            },
        )
        await logout(self.consumer.scope)
        await self.__update_player_status(False)
        self.__init_state_var()
        await self.__send_message_to_client("You have been logged out")

    async def handle_command(self, text_data: str) -> None:
        """
        Handles the command sent by the user

        Args:
            text_data (str): The command sent by the user
        """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        command_event, args = CommandParser.parse_command(message, self.is_user_authenticated)
        # Convert it to lower case to make it case insensitive
        if command_event in self.command_handlers:
            command_handler = self.command_handlers[command_event]
            logger.debug(f"Command handler for {command_event} is {command_handler}")
            await command_handler(**args)
        else:
            logger.debug(f"Command {command_event} not found")
            await self.__invalid_command(message)

    async def on_disconnect(self, close_code: int):
        """
        Disconnect the user from the game

        Args:
            close_code (int): The close code of the connection
        """
        # Log out the user if they are logged in
        if self.is_user_authenticated:
            logger.debug("User is authenticated..Logging out on disconnect")
            await self.__quit()

    async def __broadcast_message(self, message: str) -> None:
        """
        Broadcast the message to all the users

        Args:
            message (str): The message to be broadcasted
        """
        logger.debug(f"Broadcasting message : {message}")
        await self.consumer.send(text_data=json.dumps({"message": message}))

    async def __send_message_to_client(self, message: str) -> None:
        """
        Sends the message to the client

        Args:
            message (str): The message to be sent
        """
        logger.debug(f"Sending message to client : {message}")
        await self.consumer.send(text_data=json.dumps({"message": message}))

    async def __create_new_user(self, name: str, password: str) -> None:
        """Creates a new user

        Args:
            name (str): The name of the user
            password (str): The password of the user
        """
        await self.__create(name, password)
        pass

    async def __help(self):
        """
        Displays the help message
        """
        available_commands = CommandParser.get_available_commands(self.is_user_authenticated)
        available_commands = ", ".join(available_commands)
        await self.__send_message_to_client(f"Available commands are: <b>{available_commands}<b>")
        pass

    async def __invalid_command(self, message: str) -> None:
        """
        Displays the invalid command message

        Args:
            message (str): The message to be sent
        """
        error_message = f"""Command <b>{message}</b> is not available. Type "help" for help."""
        await self.__send_message_to_client(error_message)
