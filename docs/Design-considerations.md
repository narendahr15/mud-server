# Design Considerations

## Disclaimer

The design decisions are heavily influenced by the design of Evennia MUD server. Evennia is a free MUD server software that is open source and free to use. Evennia is used a reference for the design decisions of the MUD server.

A simple MUD server could be compared with a IRC chat room with additional features like character creation, login, and chat.

## Platform

The initial design of the server was made for the server to be run on the same computer as the clients. This was done to make it easier to test the server and to make it easier to run the server on a different computer.

And Ubuntu Linux(20.04.01) was used as the platform for the server. The server was tested on Ubuntu Linux and it should work on Windows and Mac. But the server needs to be tested on other platforms to make sure it works on other platforms.

The docker-compose.yml file was used to run the server and the clients. Docker was chosen to make it easier to run the server on a different platforms. And the dependencies were installed using pip and carefully chosen to avoid conflicts or specific dependencies tied to a specific platform.

## Asynchronous Connection

Websockets are used to communicate between the server and the clients. The connection betweem the client and server is always open till one of the two ends disconnects.

The server is designed to be run asynchronously. This means that the server will not wait for the client to send a command. Instead, the server will send the command to the client and the client will send the command to the server. This is done to make the server more responsive.

One of the key considerations in choosing the server framework is that how easy is to make server asynchronous. We could use Python's AsyncIO library to make the server asynchronous but we need to add a lot of boiler plate code to make it work.

Lot of candidates were considered for the server framework. e.g Twisted, quart-trio etc. But the one that was chosen was Django Channels. The Django Channels framework was chosen because it is easy to create a asynchronous server and it provides simple abstractions to handle the connections. Djano Channels uses Redis as the backend to store the connections.

## WebSockets

We use WebSockets to communicate between the server and the clients. At this stage, the server only supports WebSockets without encryption and not other protocols.

## Database/Persistence

Another key consideration in choosing the server framework is the support for the database. One of the requirement of the MUD server is that the server has to store the state of the player/objects and retrieve it later. We could use a relational database like MySQL or PostgreSQL but we need to add a lot of boiler plate code to make it work.

We chose sqlite3 as the database because it is easy to use and it is supported by Django ORM. We don't access the database directly but we use the ORM to access the database.

One disadvantage of sqlite3 is that it is a file based database. This means that the server will not be able to run on a different computer. But we can replace the Sqlite3 database with a database like Postgres to scale the server.

## Memory

Game server should be able to run on a computer with decent memory. The server should be able to store the state of the player/objects and retrieve it later. Multiple clients should be able to connect to the server.

## Game Tick

There is no game tick in the server. The server is designed to be run asynchronously. Only events from the user can trigger actions. But in the future, we can add a game tick to the server to make the gameplay more realistic.

## Logging

The MUD server uses Django logging to format and handle the logs. All the logs are displayed in the terminal. The logs can be filtered based on the severity level. The logs can also be saved to a file by modifying the settings.py file.

## Security

At this stage, the server supports only plain text authentication. The server does not support any encryption. The server uses basic Django authentication. We have to improve the security of the server by adding encryption and strong authentication mechanisms.

## Client

The client is a web browser that is used to play the MUD. The client is written in JavaScript. The client is a repurposed version of a chat client. The client is written with basic HTML and JavaScript.

## Testing

Pytest is used to test the server. The tests are written in Python. The tests are written in the tests/ directory in each module.
