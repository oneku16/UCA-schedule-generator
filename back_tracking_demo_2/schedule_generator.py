from typing import List
from back_traking_demo_1.objects.subject import Subject
from back_traking_demo_1.objects.rooms import Rooms


class ScheduleGenerator:
    __slots__ = '_subjects', '_rooms', '_schedule'

    def __init__(self, subjects):
        self._subjects = sorted(subjects, key=lambda subject: (subject.subject_pattern.counter, [pattern.number_of_classes for pattern in subject.subject_pattern.patterns]), reverse=True)
        self._rooms = Rooms().rooms
        self._schedule = []

    @property
    def get_all_subjects(self) -> List[Subject]:
        return self._subjects

    @property
    def get_all_rooms(self) -> List[Rooms]:
        return self._rooms

    def test(self):
        for room in self._rooms:
            print(room.room_name, end=':\n')
            for day in room.days:
                print('    ', day.day)
