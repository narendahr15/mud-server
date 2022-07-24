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
   Container_Boundary(web_server, "Web Server", "ASGI", "Server to communicate with the clients") {
      Container(django, "Django Server", "Django server", "Server for the MUD")
      Container(async_consumer1, "Async WebSocket Consumer1")
      Container(async_consumer2, "Async WebSocket Consumer2")
      Container(async_consumerN, "Async WebSocket ConsumerN")
   }
   ContainerQueue(redis, "Redis Backend", "Redis for Django channel", "Allows the clients to communicate with each other")
   ContainerDb(database, "Database", "Database", "Stores the game state")
}


Rel(user1, django, "Uses", "WS")
Rel(user2, django, "Uses", "WS")
Rel(userN, django, "Uses", "WS")

Rel(django, async_consumer1, "Creates")
Rel(django, async_consumer2, "Creates")
Rel(django, async_consumerN, "Creates")

Rel(async_consumer1, database, "Uses", "ORM")
Rel(async_consumer2, database, "Uses", "ORM")
Rel(async_consumerN, database, "Uses", "ORM")

Rel(async_consumer1, redis, "Uses", "Channel")
Rel(async_consumer2, redis, "Uses", "Channel")
Rel(async_consumerN, redis, "Uses", "Channel")
@enduml
```
