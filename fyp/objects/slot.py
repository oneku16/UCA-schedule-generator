from collections import Counter

from .subject import Subject


class Slot:
    def __init__(self):
        self.slot: dict[int, dict[str, Subject]] = dict()

    def __setitem__(self, index: int, params: dict[str, Subject]) -> None:
        assert 0 <= index <= 3
        for key, value in params.items():
            if index not in self.slot:
                self.slot[index] = dict()
            self.slot[index][key] = value

    def __getitem__(self, index: int) -> dict[str, Subject]:
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
