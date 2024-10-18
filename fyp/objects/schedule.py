from typing import Iterator

from .slot import Slot

from config import DAYS


class Schedule:
    def __init__(self):
        self.schedule: dict[str, Slot] = {day: Slot() for day in DAYS}

    def __iter__(self) -> Iterator[str, Slot]:
        for day, slot in self.schedule.items():
            yield day, slot

    def add_subject(self, day, quarter, mapped_objects: dict[str, object]) -> None:
        self.schedule[day].add_subject(
            quarter=quarter,
            mapped_objects=mapped_objects,
        )
