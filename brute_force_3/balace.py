from dataclasses import dataclass, field
from config import PRIORITY, DAYS, QUARTERS
import numpy as np


@dataclass
class Prices:
    room_map: np.zeros
    quarter_index: int
    day_index: int
    empty_quarter: bool = True
    price: list = field(default_factory=lambda: np.zeros([4]))
    left_neighbor: float | None = field(init=False)
    right_neighbor: float | None = field(init=False)
    subjects_in_quarter: int | None = field(init=False)
    subjects_in_days: int | None = field(init=False)

    def __post_init__(self):
        self.subjects_in_quarter = self.__count_subjects_in_quarter()
        self.subjects_in_days = self.__count_subjects_in_days()
        self.left_neighbor = self.__count_neighbors_for_left()
        self.right_neighbor = self.__count_neighbors_for_right()

    @property
    def get_price(self, priority=None):
        if priority is None:
            priority = PRIORITY.copy()
        self.price[priority['right_slot']] = self.right_neighbor
        self.price[priority['left_slot']] = self.left_neighbor
        self.price[priority['subjects_in_days']] = self.subjects_in_days
        self.price[priority['subjects_in_quarter']] = self.subjects_in_quarter
        return self.price

    def __count_subjects_in_quarter(self):
        return self.quarter_iterator(self.room_map[:, self.day_index])

    def __count_subjects_in_days(self):
        return self.quarter_iterator(self.room_map[self.quarter_index, :])

    @staticmethod
    def quarter_iterator(column):
        counter = .0
        for val in column:
            if not np.isnan(val):
                counter += val
        if any(item == .0 for item in column):
            return counter
        return False

    def __count_neighbors_for_left(self):
        if self.day_index == 0:
            return None
        return self.quarter_iterator(self.room_map[:, self.day_index - 1])

    def __count_neighbors_for_right(self):
        if self.day_index == len(DAYS) - 1:
            return None
        return self.quarter_iterator(self.room_map[:, self.day_index + 1])


@dataclass
class Tools:
    prices: Prices


class Balancer:
    __slots__ = ('__room_map',)

    def __init__(self, room_map=None):
        if room_map is None:
            self.__room_map = np.zeros([4, 5])
        else:
            self.__room_map = room_map

    def __get_slot(self, quarter_index, day_index):
        tools = Tools(Prices(room_map=self.room_map, quarter_index=quarter_index, day_index=day_index))
        return tools

    def __get_empty_slots(self):
        slots = dict()
        for quarter_index in range(len(QUARTERS)):
            for day_index in range(len(DAYS)):
                if self.room_map[quarter_index, day_index] == .0:
                    tools = self.__get_slot(quarter_index, day_index)
                    slots[(quarter_index, day_index)] = {'price': tools.prices.get_price, 'tools': tools}
        slots = {
                key: value for key, value in sorted(
                    slots.items(),
                    key=lambda item: (
                            # min(
                            -item[-1]['price'][PRIORITY['left_slot']] - item[-1]['price'][PRIORITY['right_slot']],
                            -item[-1]['price'][PRIORITY['left_slot']] is None or item[-1]['price'][PRIORITY['right_slot']],
                            # ),
                            item[-1]['price'][PRIORITY['subjects_in_quarter']],
                            item[-1]['price'][PRIORITY['subjects_in_days']],

                    ),
                    reverse=True
                )
        }
        return slots or None

    def __balance(self):
        ...

    def __fitness(self):
        ...

    @property
    def get_slot(self) -> tuple[int, int]:
        return next(iter(self.__get_empty_slots()))

    @property
    def room_map(self) -> np.zeros:
        return self.__room_map
