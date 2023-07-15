from back_tracking_demo_2.objects.subject import Subject
from config import DAYS
from brute_force_2.room.room import Room

from typing import List


class Print:
    __slots__ = ('__rooms', '__structure')

    def __init__(self, rooms: List[Room]):
        self.__rooms = rooms
        self.__structure = dict()

    def get_structured(self):
        for room in self.__rooms:
            self.__structure[room.room_name] = dict()
            for DAY in DAYS:
                try:
                    room.slot.days.get(DAY).quarters
                except AttributeError:
                    pass
                self.__structure[room.room_name][DAY] = []
                for index, item in room.slot.days.get(DAY).quarters.items():
                    if not item.status:
                        h = item.hour
                        m = item.minute
                        s: Subject = item.subject

                        self.__structure[room.room_name][DAY].append({'title': s.title, 'instructor': s.instructors.primary.instructor_name,'start': f'{h}:{m}', 'duration': None})
        return self.__structure

