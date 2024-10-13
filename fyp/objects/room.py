from bisect import bisect_right, bisect_left
from collections import defaultdict

from config import ROOMS
from slot import Slot


class Room:
    def __init__(self, room_id: str, room_name: str, capacity: int, room_type: str):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self.room_type = room_type
        self.slot = Slot()

    def is_for_subject(self, subject_type: str) -> bool:
        return subject_type == self.room_type

    def is_possible(self) -> bool:
        ...


class Rooms:
    def __init__(self, rooms: dict[str, Room]):
        self.rooms: defaultdict[str, list[Room]] = defaultdict(list)
        self.memo: defaultdict[str, defaultdict[str, Room]] = defaultdict(defaultdict)

    @property
    def real_rooms(self) -> defaultdict[str, list[Room]]:
        if not self.rooms:
            for room in ROOMS:
                room_instance = Room(**room)
                self.rooms[room_instance.room_type].append(room_instance)
            for key, value in self.rooms.items():
                self.rooms[key].sort(key=lambda item: (item.capacity, item.room_id))
        return self.rooms

    def get_room(self, subject_type: str, subject_id: str, group_size: int) -> Room:
        # if
        try:
            rooms_list = self.real_rooms[subject_type]
            start_index = bisect_left(rooms_list, group_size, key=lambda x: x.capacity)


        except KeyError:
            raise KeyError(f'Room with {subject_type} type does not exist')
