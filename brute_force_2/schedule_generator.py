from brute_force_2.subject.subject import Subject
from brute_force_2.subject.pattern import Pattern
from brute_force_2.subject.intructors import Instructors
from brute_force_2.room.room import Room
from brute_force_2.room.day import Slots, Quarters
from config import DAYS, SUBJECT_PATTERNS

from random import randint, choice, shuffle
from functools import reduce

from typing import List, Dict, Any
from pprint import pprint
from dataclasses import dataclass, field


class Balanced:
    __slots__ = ('__subject', )

    @dataclass
    class _Days:
        @dataclass
        class Day:
            status: bool = True
            classes: int = 0

        monday: Day = field(default_factory=Day)
        tuesday: Day = field(default_factory=Day)
        wednesday: Day = field(default_factory=Day)
        thursday: Day = field(default_factory=Day)
        friday: Day = field(default_factory=Day)

    def __init__(self, subject: Subject):
        self.__subject: Subject = subject

    def get_balanced(self) -> List[Pattern]:
        lecture = 0
        tutorial = 0
        laboratory = 0

        days = self._Days()

        for pattern in self.__subject.patterns:
            if pattern.subject_type == 'lecture':
                lecture = pattern.classes
            if pattern.subject_type == 'tutorial':
                tutorial = pattern.classes
            if pattern.subject_type == 'laboratory':
                laboratory = pattern.classes
        if tutorial:
            days.friday.status = False
            days.friday.classes += tutorial
        if lecture:
            days.monday.status = False
            days.monday.classes += 1
            if lecture >= 2:
                ...

        return []


class ScheduleGenerator:
    __slots__ = ('rooms', 'subjects', 'used_subjects', 'used_rooms')

    def __init__(self, *, rooms, subjects):
        self.rooms: List[Room] = rooms
        self.subjects: List[Subject] = subjects
        self.used_subjects = [False] * len(self.subjects)
        self.used_rooms = [False] * len(self.rooms)

    def test(self, subject: Subject):
        balanced = Balanced(subject)
        print(f'{ScheduleGenerator.__name__}: {ScheduleGenerator.test.__name__}')
        print(balanced.get_balanced())
        ...

    def generate(self):
        if all(self.used_subjects):
            return self.rooms

        for subject_index in range(len(self.subjects)):
            ...

    @staticmethod
    def slot_conflict(duration: int, quarters: Quarters) -> bool:
        calculate = lambda quarter_1, quarter_2: \
            quarters.quarters.get(quarter_1).status and \
            quarters.quarters.get(quarter_2).status
        if duration in (180,):
            before_lunch = calculate(1, 2)
            after_lunch = calculate(3, 4)
            if before_lunch or after_lunch:
                ...
            return False
        return True if any([quarter.status for quarter in quarters.quarters.values()]) else False

    @staticmethod
    def balance_conflict(subject: Subject, room: Room) -> bool:
        return False

    def sort_based(self, rooms_hashed: Dict) -> List[Any]:
        preferred_room = dict()
        for subject in self.subjects:
            # print(subject.title)
            if subject.title == 'Physical training':
                # print(rooms_hashed.get('bubble'))
                continue
            for pattern, required_room in zip(subject.patterns, SUBJECT_PATTERNS):
                if required_room == 'tutorial':
                    required_room = 'lecture'
                for index_room, room in enumerate(rooms_hashed.get(required_room)):
                    # print(room)
                    ...

        return list()

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
