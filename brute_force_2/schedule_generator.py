from brute_force_2.subject.subject import Subject
from brute_force_2.subject.pattern import Pattern
from brute_force_2.subject.intructors import Instructors
from brute_force_2.room.room import Room
from brute_force_2.room.day import Slots
from config import DAYS

from random import randint, choice, shuffle
from functools import reduce

from typing import List


class ScheduleGenerator:
    __slots__ = ('rooms', 'subjects', 'used_subjects', 'used_rooms')

    def __init__(self, *, rooms, subjects):
        self.rooms: List[Room] = rooms
        self.subjects: List[Subject] = subjects
        self.used_subjects = [False] * len(self.subjects)
        self.used_rooms = [False] * len(self.rooms)

    def generate(self):
        if all(self.used_subjects):
            return self.rooms

        for subject_index in range(len(self.subjects)):
            ...

    def random_based(self):
        def is_possible(room_obj: Room, day: str, quarter_id: int) -> bool:
            return room_obj.slot.days.get(day).slot_available(quarter_id)

        subjects: List[Subject] = self.subjects.copy()
        rooms: List[Room] = self.rooms.copy()
        shuffle(subjects)

        for subject in subjects:
            for _ in range(reduce(lambda a, b: a + b, [pattern.classes for pattern in subject.patterns])):
                def recursion():
                    _room = randint(0, len(rooms) - 1)
                    _day = choice(DAYS)
                    _slot = randint(1, 4)
                    if is_possible(rooms[_room], _day, _slot):
                        return _room, _day, _slot
                    return recursion()

                room, day, slot = recursion()
                rooms[room].slot.days.get(day).reserve_slot(slot, subject)

        return rooms

    def is_possible(self, room_index: int, day: str, quarter_id: int) -> bool:
        return self.rooms[room_index].slot.days.get(day).slot_available(quarter_id)
