"""
Consumers for the client.

Each client has a consumer that listens for messages from the server. 
The consumer is responsible for handling the messages and updating the 
client's state.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from game.engine import game_engine


class AsyncWebConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    def __init__(self) -> None:
        """
        Initialize the AsyncWebsocketConsumer
        """
        super().__init__()
        self.game_engine = game_engine.GameEngine(self, get_channel_layer())

    async def connect(self):
        """
        Connect to the websocket
        """
        await self.accept()

    async def disconnect(self, close_code):
        """
        Disconnect from the websocket

        Args:
            close_code: The close code of the websocket
        """
        await self.game_engine.on_disconnect(close_code)
        await self.send(text_data=json.dumps({"message": "Goodbye"}))
        await self.close()

    async def receive(self, text_data):
        """
        On receive of a message from the websocket

        Args:
            text_data (str): The message from the websocket
        """
        await self.game_engine.handle_command(text_data)

    async def message_location(self, event):
        """
        Message handler to broad cast the message to the users in the same location

        Args:
            event : The event from the channel layer
        """
        if self.game_engine.is_user_authenticated:
            location = self.game_engine.room.id
            # Only publish message to the current room
            if event["location"] == location:
                await self.send(text_data=json.dumps({"message": event["message"]}))

    async def message_broadcast(self, event):
        """
        Message handler to broad cast the message to all the users

        Args:
            event: The event from the channel layer
        """
        if self.game_engine.is_user_authenticated:
            await self.send(text_data=json.dumps({"message": event["message"]}))
