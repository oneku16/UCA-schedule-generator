from typing import List
from back_traking.configs import ROOMS
from back_traking.data_types.slots import Slots


class Rooms:
    __slots__ = '_rooms'

    class __Room:
        __slots__ = '_room_id', '_capacity', '_room_type', '_room_name', '_days'

        def __init__(self, room_id, capacity, room_type, room_name):
            self._room_id = room_id
            self._capacity = capacity
            self._room_type = room_type
            self._room_name = room_name
            self._days = Slots().days

        @property
        def room_id(self):
            return self._room_id

        @property
        def capacity(self):
            return self._capacity

        @property
        def room_type(self):
            return self._room_type

        @property
        def room_name(self):
            return self._room_name

        @property
        def days(self):
            return self._days

        @property
        def priority(self):
            if self._room_type == 'bubble':
                return 0
            elif self._room_type == 'lecture':
                return 1
            return 2

    def __init__(self):
        self._rooms = self.__generate_rooms()
        self.rooms.sort(key=lambda room: (room.priority, room.capacity), reverse=True)

    @property
    def rooms(self):
        return self._rooms

    def __generate_rooms(self) -> List[__Room]:

        def _wrapper():
            for room in ROOMS:
                yield self.__Room(**room)

        return list(_wrapper())
