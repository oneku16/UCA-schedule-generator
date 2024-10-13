from copy import deepcopy

from config import SLOTS


class Slot:

    def __init__(self):
        self.slots: dict[str, str | int] = dict()
        self.reserved = dict[str, str | str] = dict()

    @property
    def real_slots(self):
        if not self.slots:
            self.slots = deepcopy(SLOTS)
            for slot in SLOTS:
                slot['is_reserved'] = False
                slot['subject'] = None
        return self.slots

    def is_empty(self) -> bool:
        return len(self.slots) != len(self.reserved)

    def reserve(self, subject_id, start_time, end_time) -> None:
        ...
