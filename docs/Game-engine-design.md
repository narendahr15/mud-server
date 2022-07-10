# Game engine/state design

The game engine has a one to one association with the AsyncWebSocketConsumer. The AsyncWebSocketConsumer is the class that handles the connection between the server and the client. The AsyncWebSocketConsumer is responsible for handling the messages from the client and sending the messages to the server.

The game engine does not have a tick mechanism. The game engine is designed to be run asynchronously. The game engine is responsible for handling the events from the user.

The game engine has a client-attorney pattern with the AsyncWebSocketConsumer.

```plantuml
@startuml

!theme plain
top to bottom direction
skinparam linetype ortho

class Exits {
   id: int
   name: str
   location: int
   destination: int
}

class Room {
    id: int
    name: str
    desc: str
    exits: Exits
}

class MapNavigator {
   +get_default_room_id()
   +get_room_by_id(id: int)
   +move_to(id: int)
   +get_room_name()
   +get_printable_room_exits()
}

MapNavigator --* Room
Room --* Exits

class commands.CommandParser {
   +parse(command: str, is_user_authenticated : bool) -> GameEngineEvent, dict
   +get_commands(is_user_authenticated : bool) -> list
}

class AsynWebSocketConsumer {
   game_engine: GameEngine
    +connect(url: String)
    +disconnect()
    +recieve(message: String)
    +message_location(self, event)
    message_broadcast(self, event)
}

class GameEngine {
   command_handlers: dict
   is_user_authenticated: bool
   channel_layer: Channel
   consumer: AsynWebSocketConsumer
   room: Room
   player: PlayerProfile
   username: str
   -- public functions: --
   __init__(self, consumer, channel_layer):
   handle_command(self, text_data: str):
   on_disconnect(self, close_code: int):
   -- private functions: --
   __init_state_var(self):
   -- ORM helpers --
   __create_user(self, name: str, password: str):
   __get_user(self, name: str):
   __get_player_profile(self, user: User):
   __get_users_in_location(self, location: int):
   __update_player_status(self, connected: bool):
   __update_location(self, location: int):
   __create(self, name: str, password: str):
   __login(self, name: str, password: str):
   __create_new_user(self, name: str, password: str):
   -- command handlers --
   __register_user(self, username: str, password: str):
   __connect_user(self, username: str, password: str):
   __say(self, message: str):
   __move_to(self, direction: str):
   __look(self):
   __quit(self):
   __help(self):
   -- Consumer helpers --
   __broadcast_message(self, message: str):
   __send_message_to_client(self, message: str):
   __invalid_command(self, message: str):
}

GameEngine --* AsynWebSocketConsumer
AsynWebSocketConsumer --* GameEngine
GameEngine --o MapNavigator
GameEngine --o commands.CommandParser

@enduml
```
