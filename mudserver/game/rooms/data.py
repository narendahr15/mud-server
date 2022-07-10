"""
File to store the data of the rooms.
"""
room_data = {
    "rooms": [
        {
            "id": 1,
            "name": "Just outside the k6 virtual offices",
            "desc": "The k6 office building towers above you, disappearing into virtual clouds high above.",
        },
        {
            "id": 2,
            "name": "The ridiculously large lobby",
            "desc": "The k6 lobby stretches far in every direction. The exits are so far away that they almost dip below the horizon.\nThere's friendly sign here though, welcoming you.",
        },
        {
            "id": 3,
            "name": "A lush terrarium",
            "desc": "In the center of this office space is a huge glass terrarium. Inside are crocodiles, relaxing under an artiticial sun.\nOne side-hatch of the terrarium is left open and there is a wet trail leading westwards. Noone seem too bothered.",
        },
        {
            "id": 4,
            "name": "The water cooler",
            "desc": "This is clearly the heart of the k6 offices. People gathers here to chat and have Swedish 'fika' around a virtually huge water cooler.",
        },
        {
            "id": 5,
            "name": "The backend machine room",
            "desc": "This room is full of virtual machinery. Steam hisses from the Flask install in the corner while an imposing wall of Django blinks along the side.\nIn the center of the room, the backend devs are cheering two crocodiles running in a hamster wheel and keeping the lights on.",
        },
    ],
    "exits": [
        {"id": 1, "name": "west", "location": 1, "destination": 2},
        {"id": 2, "name": "north", "location": 2, "destination": 3},
        {"id": 3, "name": "west", "location": 2, "destination": 4},
        {"id": 4, "name": "east", "location": 2, "destination": 1},
        {"id": 5, "name": "west", "location": 3, "destination": 5},
        {"id": 6, "name": "south", "location": 3, "destination": 2},
        {"id": 7, "name": "east", "location": 4, "destination": 2},
        {"id": 8, "name": "north", "location": 4, "destination": 5},
        {"id": 9, "name": "east", "location": 5, "destination": 3},
        {"id": 10, "name": "south", "location": 5, "destination": 4},
    ],
}
