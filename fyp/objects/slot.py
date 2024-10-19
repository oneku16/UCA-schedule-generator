from collections import Counter
from random import choice
from typing import (
    Any,
)

from ..exceptions import NoEmptySlotError


class Slot:
    def __init__(self):
        self.slot: dict[int, dict[str, object]] = dict()

    def add_subject(self, quarter: int, mapped_objects: dict[str, object]) -> None:
        assert 0 <= quarter <= 3
        if self.is_full():
            raise NoEmptySlotError()
        for key, value in mapped_objects.items():
            if quarter not in self.slot:
                self.slot[quarter] = dict()
            self.slot[quarter][key] = value

    def get_empty_quarters(self) -> set[int]:
        quarters = set()
        for quarter in range(4):
            if quarter not in self.slot:
                quarters.add(quarter)
        return quarters

    def transfer_subjects(
            self,
            target_slot: "Slot",
            quarters: list[int],
            random: bool = True,
            **params: dict[str, Any],
    ) -> None:
        empty_quarters = target_slot.get_empty_quarters()
        assert len(empty_quarters) >= len(quarters)

        for quarter in quarters:
            values = self.slot.pop(quarter)
            if random:
                random_quarter = choice(list(empty_quarters))
                empty_quarters.remove(random_quarter)
                target_slot.add_subject(quarter, values)
            else:
                raise NotImplementedError


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
    def subjects_list(self) -> list[dict[str, object]]:
        subjects_list = list()
        for quarter in self.slot.values():
            subjects_list.append(quarter)
        return subjects_list

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
