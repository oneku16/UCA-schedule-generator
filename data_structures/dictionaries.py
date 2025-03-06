from collections import defaultdict
from typing import Generator

from constraints.instructor import Instructor
from constraints.room import Room
from constraints.slot import Slot
from constraints.subject import Subject


class ScheduleDictionary:
    __slots__ = (
        "map",
    )
    def __init__(self):
        self.map: defaultdict[str, list[list[Subject, Slot, Room, Instructor]]] = defaultdict(list)

    def __setitem__(
            self,
            subject_id,
            subject: list[Subject, Slot, Room, Instructor],
    ):
        self.map[subject_id].append(subject)

    def __getitem__(self, subject_id):
        return self.map[subject_id]

    def __contains__(self, subject_id):
        return subject_id in self.map

    def __repr__(self):
        return repr(self.map)

    def __iter__(self) -> Generator[tuple[str, list[list[Subject, Slot, Room, Instructor]]], None, None]:
        for subject_id, subject in self.map.items():
            yield subject_id, subject
