import numpy as np
import pandas as pd
from config import DAYS, QUARTERS
from random import choice, randint
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Prices:
    room: np.zeros
    day_index: np.int
    quarter_index: np.int
    empty_quarter: np.bool = True
    __price: np.float = .0
    left_neighbor: np.float = field(init=False)
    right_neighbor: np.float = field(init=False)
    subjects_in_quarter: np.int = field(init=False)
    subjects_in_days: np.int = field(init=False)

    def __post_init__(self):
        self.subjects_in_quarter = self.__count_subjects_in_quarter()
        self.subjects_in_days = self.__count_subjects_in_days()
        self.left_neighbor = 0.0
        self.right_neighbor = 0.0

    @property
    def price(self):
        self.__price -= 1
        return self.__price

    def __count_subjects_in_quarter(self):
        indexed = next(iter(QUARTERS)) == 1
        counter = 0
        for quarter_index in QUARTERS:
            if self.room[self.day_index][quarter_index - indexed] is not np.nan:
                counter += self.room[self.day_index][quarter_index - indexed]
        return counter

    def __count_subjects_in_days(self):
        counter = 0
        for day_index in range(len(DAYS)):
            if self.room[day_index][self.quarter_index] is not np.nan:
                counter += self.room[day_index][self.quarter_index]
        return counter

    def __count_neighbors(self):
        counter_left = counter_right = 0
        if self.day_index >= 1:
            for quarter_index in range(len(QUARTERS)):
                if self.room[quarter_index][self.day_index - 1] is not np.nan:
                    counter_left += self.room[quarter_index][self.day_index - 1]
        return counter_left, counter_right


@dataclass
class Tools:
    prices: int


class Balancer:
    __slots__ = ('__room', '__days', '__quarters')

    def __init__(self, room=None):
        self.__room = room
        self.__days = DAYS
        self.__quarters = (1, 2, 3, 4)

    def __balance(self):
        ...

    def __fitness(self):
        ...

    @property
    def get_quarter_index(self, index_mode=False) -> tuple[str, int]:
        return next(iter(self.__days)), 0 - int(index_mode)

    @property
    def room(self) -> np.zeros:
        return self.__room

    @room.setter
    def room(self, room: np.zeros):
        self.__room = room


def main():
    room = np.zeros([5])

    room[0] = 1
    room[1] = np.nan
    room[2] = 1


if __name__ == '__main__':
    main()