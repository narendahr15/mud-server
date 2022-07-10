import pytest
import game.rooms.map_navigator as map_navigator


def test_get_default_room():
    assert map_navigator.MapNavigator.get_default_room_id() != None


@pytest.mark.parametrize(
    "room_id",
    [(1), (2), (3), (4), (5)],
)
def test_get_room(room_id):
    room = map_navigator.MapNavigator.get_room(room_id=room_id)
    assert room != None
    assert room.id == room_id
    assert room.name != None
    assert room.desc != None


def test_get_room_not_found():
    room = map_navigator.MapNavigator.get_room(room_id=-1)
    assert room == None


@pytest.mark.parametrize(
    "current_location_id, direction, expected_location_id",
    [(1, "west", 2), (2, "north", 3), (3, "west", 5), (4, "east", 2)],
)
def test_move_to(current_location_id, direction, expected_location_id):
    assert (
        map_navigator.MapNavigator.move_to(current_location_id, direction) == expected_location_id
    )


@pytest.mark.parametrize(
    "room_id",
    [(1), (2), (3), (4), (5)],
)
def test_get_room_name(room_id):
    room_name = map_navigator.MapNavigator.get_room_name(room_id=room_id)
    assert room_name != None


def test_get_room_name_not_found():
    room_name = map_navigator.MapNavigator.get_room_name(room_id=-1)
    assert room_name == None
