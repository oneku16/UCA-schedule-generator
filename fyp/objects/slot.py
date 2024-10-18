from collections import Counter
from typing import (
    Any,
    Iterable,
)

from ..exceptions import NoEmptySlotError


class Slot:
    def __init__(self):
        self.slot: dict[int, dict[str, object]] = dict()

    def add_subject(self, quarter, mapped_objects: dict[str, object]) -> None:
        assert 0 <= quarter <= 3
        if self.is_full():
            raise NoEmptySlotError()
        for key, value in mapped_objects.items():
            if quarter not in self.slot:
                self.slot[quarter] = dict()
            self.slot[quarter][key] = value

    def get_empty_quarters(self) -> list[int]:
        quarters = list()
        for quarter in range(4):
            if quarter not in self.slot:
                quarters.append(quarter)
        return quarters

    def transfer_subjects(
            self,
            target_slot: "Slot",
            *quarters: Iterable[int],
            **params: dict[str, Any]
    ) -> None:
        ...

    def __setitem__(self, index: int, params: dict[str, object]) -> None:
        assert 0 <= index <= 3
        for key, value in params.items():
            if index not in self.slot:
                self.slot[index] = dict()
            self.slot[index][key] = value

    def __getitem__(self, index: int) -> dict[str, object]:
        assert 0 <= index <= 3
        return self.slot[index]

    def __delitem__(self, index: int):
        assert 0 <= index <= 3
        del self.slot[index]

    def __contains__(self, index) -> bool:
        assert 0 <= index <= 3
        return index in self.slot

    def __repr__(self):
        return str(self.slot)

    def __iter__(self):
        for index, slot in self.slot.items():
            yield index, slot

    def __len__(self) -> int:
        return len(self.slot)

    def is_empty(self) -> bool:
        return len(self.slot) == 0

    def is_full(self) -> bool:
        return len(self.slot) == 4

    @property
    def subjects(self) -> Counter:
        counter = Counter()
        for slot in self.slot.values():
            if not slot:
                continue
            for key, value in slot.items():
                if key == 'subject':
                    counter[value.subject_id] += 1
        return counter
