from dataclasses import dataclass, field
from typing import Any

from brute_force_2.subject.subject import Subject
from config import SLOTS, DAYS


class Slots:
    __slots__ = ('__days',)

    def __init__(self):
        self.__days = {day: Quarters() for day in DAYS}

    @property
    def days(self):
        return self.__days


class Quarters:
    __slots__ = ('__quarters', '__stack', '__day_name')

    @dataclass(kw_only=True, slots=True)
    class QuarterHandler:
        hour: str
        minute: str
        duration: int
        quarter_id: int
        subject: Subject = field(init=False, default=None)
        status: bool = field(init=False, default=True)

    def __init__(self):
        self.__quarters = {quarter_id: self.QuarterHandler(**slot, quarter_id=quarter_id) for quarter_id, slot in enumerate(SLOTS, 1)}
        self.__stack = list()

    @property
    def quarters(self):
        return self.__quarters

    def slot_available(self, quarter_id: int = None) -> bool:
        if quarter_id is None:
            return any(slot.status for slot in self.__quarters.values())
        assert 1 <= quarter_id <= 4
        return self.__quarters.get(quarter_id).status

    def not_reserved_slots(self) -> tuple[Any, ...]:
        return tuple(quarter_id for quarter_id, slot in self.__quarters.items() if slot.status)

    def reserve_slot(self, quarter_id: int, subject: Subject) -> None:
        if self.slot_available(quarter_id=quarter_id):
            self.__quarters.get(quarter_id).subject = subject
            self.__quarters.get(quarter_id).status = False

    def undo_reservation(self, quarter_id: int) -> None:
        if not self.slot_available(quarter_id=quarter_id):
            self.__quarters.get(quarter_id).status = True
            self.__quarters.get(quarter_id).subject = None
