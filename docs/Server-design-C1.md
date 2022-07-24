# Server design

The server uses Django channnel to communicate with the clients. The server uses Redis as the communication backend. Each client has its own AsyncWebSocketConsumer.

```plantuml
@startuml Server design
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml


!theme spacelab
left to right direction
skinparam linetype polyline

Person(user1, "User1")
Person(user2, "User2")
Person(userN, "UserN")

Boundary(c1, "MUD Server") {
   System(web_server, "Web Server", "ASGI", "Server to communicate with the clients")
   System(database, "Database", "Database", "Stores the game state")
'    System(async_consumer1, "Async WebSocket Consumer1")
'    System(async_consumer2, "Async WebSocket Consumer2")
'    System(async_consumerN, "Async WebSocket ConsumerN")
}

Rel(user1, web_server, "Uses", "WS")
Rel(user2, web_server, "Uses", "WS")
Rel(userN, web_server, "Uses", "WS")

Rel(web_server, database, "Uses", "DB")

' Rel(web_server, async_consumer1, "Creates")
' Rel(web_server, async_consumer2, "Creates")
' Rel(web_server, async_consumerN, "Creates")

' Rel(async_consumer1, database, "Uses")
' Rel(async_consumer2, database, "Uses")
' Rel(async_consumerN, database, "Uses")

@enduml
```
