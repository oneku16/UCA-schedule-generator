from brute_force_2.room.room import Room
from typing import List


class Print:
    __slots__ = '__rooms'

    def __init__(self, rooms):
        self.__rooms: List[Room] = rooms

    def print_out(self):
        for room in self.__rooms:
            print(f'room id={room.room_id} room name{room.room_name}')
            ...
