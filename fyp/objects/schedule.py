from typing import Iterator

from .slot import Slot

from config import DAYS


class Schedule:
    def __init__(self):
        self.schedule: dict[str, Slot] = {day: Slot() for day in DAYS}

    def __iter__(self) -> Iterator[tuple[str, Slot]]:
        for day, slot in self.schedule.items():
            yield day, slot

    def __getitem__(self, day: str) -> Slot:
        return self.schedule[day]

    def get_empty_slots(self) -> dict[str, list[int]]:
        day_map = dict()

        for day, slot in self.schedule.items():
            if not slot.is_full():
                quarters: list[int] = list(slot.get_empty_quarters())
                day_map[day] = quarters

        return day_map

    def add_subject(self, day: str, quarter: int, mapped_objects: dict[str, object]) -> None:
        self.schedule[day].add_subject(
            quarter=quarter,
            mapped_objects=mapped_objects,
        )

    def __repr__(self):
        return f'Schedule({self.schedule})'
