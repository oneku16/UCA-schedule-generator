from collections import defaultdict
from random import choice, randint

from schedule_generator.constraints import Room

RoomList = list[int, Room]


class RoomSelector:
    """
    A class for managing and selecting rooms based on their type and availability.

    The class maintains a dictionary of rooms grouped by their type, where each room is associated
    with a count representing its availability. Rooms can be added, removed, or selected randomly
    based on their type.

    Attributes:
        __rooms (defaultdict[str, list[tuple[int, Room]]]): A dictionary mapping room types to
            lists of tuples containing the count of available rooms and the Room instance.
    """
    __slots__ = ("__rooms",)

    def __init__(self, rooms: list[Room]):
        """
        Initializes a RoomSelector instance.

        Args:
            rooms (list[Room]): A list of Room instances to manage. Each room is initialized
                with a default count of 20.
        """
        self.__rooms: defaultdict[str, list[RoomList]] = self.build_room_structure(rooms)

    @property
    def rooms(self) -> defaultdict[str, list[RoomList]]:
        """
        Returns the internal room structure.

        Returns:
            defaultdict[str, list[tuple[int, Room]]]: A dictionary mapping room types to
                lists of tuples containing the count of available rooms and the Room instance.
        """
        return self.__rooms

    @staticmethod
    def build_room_structure(rooms: list[Room]) -> defaultdict[str, list[RoomList]]:
        """
        Builds a structured dictionary of rooms grouped by their type.

        Args:
            rooms (list[Room]): A list of Room instances.

        Returns:
            defaultdict[str, list[list[int, Room]]]: A dictionary mapping room types to
                lists of tuples containing the count of available rooms and the Room instance.
        """
        mapped = defaultdict(list)
        for room in rooms:
            mapped[room.room_type].append([20, room])  # Initialize each room with a count of 20
        return mapped

    def __update_room(self, room_type: str, index: int) -> Room:
        """
        Updates the count of a room and returns it. If the count reaches zero, the room is removed.

        Args:
            room_type (str): The type of the room.
            index (int): The index of the room in the list.

        Returns:
            Room: The selected room.
        """
        rooms = self.__rooms[room_type]
        rooms[index], rooms[-1] = rooms[-1], rooms[index]  # Swap with the last element
        rooms[-1][0] -= 1 # Decrement the count
        room = rooms[-1][1]  # Re-add the room if the count is still positive
        if rooms[-1][0] == 0:
            rooms.pop()
        return room

    def reduce_room(self, room: Room) -> None:
        """
        Reduces the count of a room by 1. If the count reaches zero, the room is removed.

        Args:
            room (Room): The room to reduce.
        """
        index = 0

        while index < len(self.__rooms[room.room_type]):
            if room.room_id == self.__rooms[room.room_type][index][1].room_id:
                self.__rooms[room.room_type][index][0] -= 1
                if self.__rooms[room.room_type][index][0] == 0:
                    continue
            index += 1

    def put_room(self, room: Room) -> None:
        """
        Increases the count of a room by 1. If the room does not exist, it is added with a count of 1.

        Args:
            room (Room): The room to add or update.
        """
        for index in range(len(self.__rooms[room.room_type])):
            if self.__rooms[room.room_type][index][1].room_id == room.room_id:
                self.__rooms[room.room_type][index][0] += 1
                return
        self.__rooms[room.room_type].append([1, room]) # Add the room if it doesn't exist

    def get_room(self, room_types: frozenset[str]) -> Room:
        """
        Randomly selects a room of the specified types.
        Args:
            room_types (frozenset[str]): The types of rooms to select from.
        Returns:
            Room: The selected room.
        """
        # Filter out 'tutorial' rooms, since 'lecture' and 'tutorial' are same.
        room_types = tuple([rt for rt in room_types if rt != 'tutorial'])

        if all(not self.__rooms[rt] for rt in room_types):
            room_types = tuple(self.__rooms.keys())

        while room_type := choice(room_types):
            if self.__rooms[room_type]:
                break

        index = randint(0, len(self.__rooms[room_type]) - 1)
        room = self.__update_room(room_type, index)

        return room
