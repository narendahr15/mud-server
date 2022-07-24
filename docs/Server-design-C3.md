# Server design

The server uses Django channnel to communicate with the clients. The server uses Redis as the communication backend. Each client has its own AsyncWebSocketConsumer.

```plantuml
@startuml Web Server
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

!theme spacelab
left to right direction
skinparam linetype polyline

Component(user1, "User1")
Container_Boundary(web_server, "Web Server", "ASGI", "Server to communicate with the clients") {
Component(AsyncWebSocketConsumer, "Async WebSocket Consumer", "Django Consumer", "Websocket wrapper")
Component(game_engine, "Game Engine", "Python module", "The game engine")
Component(command, "Command", "Python module", "Command module containing the commands")
Component(command_parser, "Command Parser", "Python module", "Command parser module")
Component(map_navigator, "Map Navigator", "Python module", "Map navigator module")
ComponentDb(map_db, "Map Database", "JSON file", "Map database")
}
ComponentDb_Ext(model_manager, "Model Manager", "Django Python module", "Model manager")
ComponentQueue_Ext(redis, "Redis", "Redis", "Redis backend")

' Server communication
Rel(user1, web_server, "Uses", "WS")
Rel(web_server, AsyncWebSocketConsumer, "Creates")

' Communication in the consumer
Rel(AsyncWebSocketConsumer, game_engine, "Creates/uses", "WS")
Rel(AsyncWebSocketConsumer, redis, "Uses", "Layers")

' Communication in the game **engine**
Rel(game_engine, redis, "Uses", "Layers")
Rel(game_engine, command_parser, "Uses")
Rel(game_engine, model_manager, "Uses")
Rel(game_engine, map_navigator, "Uses")

Rel(command_parser, command, "Uses")
Rel(map_navigator, map_db, "Uses")
@enduml
```
