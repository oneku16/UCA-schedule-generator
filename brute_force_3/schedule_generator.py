from .rooms import Room
from .patterns import SubjectPattern
from config import DAYS, SUBJECT_PATTERNS


from typing import List


class ScheduleGenerator:
    __slots__ = ('rooms', 'subjects', 'used_subjects', 'used_rooms')

    def __init__(self, *, rooms, subject_patterns):
        self.rooms: List[Room] = rooms
        self.subjects: List[SubjectPattern] = subject_patterns



