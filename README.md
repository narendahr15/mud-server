# MUD Server

A simple MUD server with a few commands to play. You could use this as a starting point for your own MUD server.

The server is designed to be simple and easy to use. It is not designed to be a full-functional MUD server.

This server is written in Python and uses the Django channels along with Redis backend to handle the communication. The server comes with an in-built MUD client that can be used to play the game.

At this stage, the server does not support other clients than the MUD client provided along with the server.

New commands can be added to the server by adding them to the `commands` dictionary and the game play can be customized by adding them to the `game` dictionary.

## Requirements

You will need to install Python (3.9+) to run the server.

To allow players to connect remotely, the server will also need to be connected to the internet.

The server also needs to be able to write to the database.

## Running the server

### Using Docker-Compose

Using docker-compose is a preferred way to run the MUD server. In the root directory of the project, from the terminal, run the following command:

```bash
# For building the base image
docker-compose build
# For migrations
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
# For running the server
docker-compose up
```

The MUD server will be running on the port `8000`. The port of the MUD server can be changed by modifying the command in the docker-compose.yml. You can connect to it by opening a browser and typing `http://localhost:8000/client/`.

### Without Docker-Compose

In the root directory of the project, from the terminal, run the following command:

```bash
# Better to use virtual environment to avoid conflicts with other packages
python3 -m venv venv
source venv/bin/activate
# For installing django and channels
cd mudserver
pip install -r requirements.txt
# Needs redis for the channel backend
docker run -d --name redis -p 6379:6379 redis
# Run the server
# The following commands are needed only for the first time or when you change/add models to the database.
python3 manage.py makemigrations
python3 manage.py migrate
# Run the server
python3 manage.py runserver 0.0.0.0:8000
# To stop the server
ctrl + c
```

**Note**: The server and the clients were tested on Ubuntu linux and it should work on Windows and Mac. But the server needs to be tested on other platforms to make sure it works on other platforms.

## Running the client

Once the server is running, you can connect to it by opening a browser and typing `http://localhost:8000/client/`. This will open a client connection to the server. Multiple clients can be connected to the server.

## Running the tests

```bash
# Better to use virtual environment to avoid conflicts with other packages
python3 -m venv venv
source venv/bin/activate
# For installing django and channels
cd mudserver
pip install -r requirements.txt
# Run the server
# The following commands are needed only for the first time or when you change/add models to the database.
python3 manage.py makemigrations
python3 manage.py migrate
pytest
```

## Design decisions

Please refer the [docs](docs) folder for the design decisions made in the creation of the server.

## Limitations

1. The current version of the server does not support multiple login of the same user. Multiple login creates undefined behavior.
2. Session persistence is not implemented.
3. Hardcoded game rooms.

## Scope of improvement

1. Support for additional protocols. For example, support for telnet, ssh, and other protocols. Now the server only supports its own protocol.
2. Separate layer for handling the Authentication. Evennia has different portals for authentication and game play.
3. In game customizable command parser, game play, and game rooms.
4. Ticks in the game engine to make it more realistic.
5. Separating the logic from the network layer. Now the game logic is tied with the network layer. Need to isolate the game logic from the network layer.
6. Coordinate system of the rooms : Cartesian, Polar, Spherical, etc.
7. Exception handling
8. Integration testing
9. Isolate string formatting from the game logic
10. Get the plantuml working in the Github markdown

## References

1. https://github.com/evennia/evennia
2. https://github.com/RanvierMUD/ranviermud
3. https://channels.readthedocs.io/en/latest/
