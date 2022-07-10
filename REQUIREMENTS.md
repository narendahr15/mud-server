# k6 Home assignment, Senior backend engineer

> (This assignment will only be given after passing the initial manager interviews).

## Overview

In this assignment you are tasked with creating a small Python
Multi-User-Dungeon (MUD) server.
A MUD is an online,
text-based multiplayer game. MUDs are the precursors to MMORPGs, with a game world shared between all players.
Interaction with the game is handled by the user entering commands in their
client. The world is asynchronous and the server may send data to the client at
any time ([more info on Wikipedia](https://en.wikipedia.org/wiki/MUD)).

This exercise tests your skills of system-design, attention to best-practices
and project-maintainability. Another important aspect when designing this is to consider
that you (or others) will want to expand on it later (more commands, bigger
game world, the ability to build new rooms from in-game, extended gameplay etc).

_Imagine you are making this as an open-source project that you expect others to be
able to contribute to and build their own games from._

## Hand-in

- You have one week to present a solution.
- Put your code in a _private_ Github repository and give read-access to users [Griatch](https://github.com/Griatch), [mpandurovic](https://github.com/mpandurovic), [lantero](https://github.com/lantero) and [sniku](https://github.com/sniku). Please also provide the url to the repo since we've had issues with github sending the invite-notifications in the past.
- We'll then schedule a 90min call to discuss your solution. This will be a Zoom call. Expect to be asked to share your screen.
- While we expect a working solution, we know that people have busy lives and different amounts of time to spend on a home exercise like this. So in the interview we will ask how much time you spent and adjust our questions and expectations accordingly.

## Resources

To limit the scope of the assignment, a working echo-server and test-client
are provided, using websockets and asyncio. A json file with game-world data is
also included.

- `client.py` - simple test MUD-client using websockets.
- `server.py` - template MUD-server set up as an echo server.
- `init_data.json` - description and topology of a small demo world.

You can modify these as much as you want, but the focus should be
on the server-side. You may use any third-party Python libraries you deem suitable
for the task, except for MUD-specific frameworks - we want to see how _you_
go about designing this.

## Expected server features

The solution should run on Python3.9+ and be able to run and be tested with
several simultaneous players on a reasonably modern laptop.

### Game loop

#### Registering and Login

- After connecting to the server, users should be able to register a new
  account.
- Once registered, they should be able to authenticate and log into the game.
- When logging in, other players in the entire game should be notified.
- When logged in (and only then), the player should have a location in the game
  world and be visible to any other players at that location.

#### In-game

- Players should be able to _look_ to see the current room's description, any
  exits to other rooms as well as other players in the same room. Think about
  how to expand this in the future!
- Players should be able to _speak_ to anyone in the same location.
- Players should be able to _move_ to adjacent rooms.
- Players should be able to get _help_ on how to do things.

#### Logout

- When logging out, other players in the entire game should be notified.
- When logging out, the player should be removed/hidden from the game world.
- A returning player should always re-appear at the location they were at when
  they logged out.

### Example command syntax

Commands are typed by the player and parsed by the server. They are usually
case-insentitive.
You can change the command syntax if you prefer something else, but here is
an example list covering the requirements:

- `register <name> <password>` - create a new account on the server.
- `login <name> <password>` - authenticate to server, notifying all players.
- `look` - view current room name and description, as well as exits and players
  in the same location. It's convenient to also allow the alias `l`.
- `say <message>` - Say something to others in the same room. Make sure it's
  clear who's speaking!
- `north/east/south/west` - move in a certain direction, to an adjacent room.
  It's convenient to also allow aliases `n`, `e`, `s`, `w`.
- `help` - show help about currently available commands.
- `quit/exit/logout` - leave the game, notifying all players.

### Game world

The assignment includes a JSON file with descriptions for five rooms and links
between them. You can use these as-is but you can also make your own same-sized
world if you prefer.

The included map looks like this:

```
#-#
| |
#-#-#
```

Above, `#` is a room and `|` and `-` indicate a two-way north-south and
west-east connection between rooms respectively. New players should probably
appear at the room in the bottom-right.

Here's an example of how the start room could be visualized
in-game (using e.g. the 'look' command):

```
Just outside the k6 virtual offices

The k6 virtual office building towers above you, disappearing into the
clouds high above.

Players: Pepe, Ana
Exit: west

```
