# import numpy as np
# import pandas as pd
# from config import DAYS, QUARTERS, PRIORITY
# from random import choice, randint
# from dataclasses import dataclass, field
#
#
# @dataclass
# class Prices:
#     room: np.zeros
#     quarter_index: int
#     day_index: int
#     empty_quarter: bool = True
#     price: list = field(default_factory=lambda: np.zeros([4]))
#     left_neighbor: float | None = field(init=False)
#     right_neighbor: float | None = field(init=False)
#     subjects_in_quarter: int | None = field(init=False)
#     subjects_in_days: int | None = field(init=False)
#
#     def __post_init__(self):
#         self.subjects_in_quarter = self.__count_subjects_in_quarter()
#         self.subjects_in_days = self.__count_subjects_in_days()
#         self.left_neighbor = self.__count_neighbors_for_left()
#         self.right_neighbor = self.__count_neighbors_for_right()
#
#     @property
#     def get_price(self, priority=None):
#         if priority is None:
#             priority = PRIORITY.copy()
#         self.price[priority['right_slot']] = self.right_neighbor
#         self.price[priority['left_slot']] = self.left_neighbor
#         self.price[priority['subjects_in_days']] = self.subjects_in_days
#         self.price[priority['subjects_in_quarter']] = self.subjects_in_quarter
#         return self.price
#
#     def __count_subjects_in_quarter(self):
#         return self.quarter_iterator(self.room[:, self.day_index])
#
#     def __count_subjects_in_days(self):
#         return self.quarter_iterator(self.room[self.quarter_index, :])
#
#     @staticmethod
#     def quarter_iterator(column):
#         counter = .0
#         for val in column:
#             if not np.isnan(val):
#                 counter += val
#         if any(item == .0 for item in column):
#             return False or counter
#         return False
#
#     def __count_neighbors_for_left(self):
#         if self.day_index == 0:
#             return None
#         return self.quarter_iterator(self.room[:, self.day_index - 1])
#
#     def __count_neighbors_for_right(self):
#         if self.day_index == len(DAYS) - 1:
#             return None
#         return self.quarter_iterator(self.room[:, self.day_index + 1])
#
#
# @dataclass
# class Tools:
#     prices: Prices
#
#
# class Balancer:
#     __slots__ = ('__room', '__days', '__quarters')
#
#     def __init__(self, room=None):
#         self.__room = room
#
#     def __get_slot(self, quarter_index, day_index):
#         tools = Tools(Prices(room=self.room, quarter_index=quarter_index, day_index=day_index))
#         return tools
#
#     def __get_empty_slots(self):
#         slots = dict()
#         for quarter_index in range(len(QUARTERS)):
#             for day_index in range(len(DAYS)):
#                 if self.room[quarter_index, day_index] == .0:
#                     tools = self.__get_slot(quarter_index, day_index)
#                     slots[(quarter_index, day_index)] = {'price': tools.prices.get_price, 'tools': tools}
#         slots = {
#                 key: value for key, value in sorted(
#                     slots.items(),
#                     key=lambda item: (
#                             item[-1]['price'][PRIORITY['subjects_in_quarter']],
#                             item[-1]['price'][PRIORITY['subjects_in_days']]
#                     ),
#                     reverse=True
#                 )
#         }
#         return slots or None
#
#     def __balance(self):
#         ...
#
#     def __fitness(self):
#         ...
#
#     @property
#     def get_slot(self) -> tuple[int, int]:
#         return next(iter(self.__get_empty_slots()))
#
#     @property
#     def room(self) -> np.zeros:
#         return self.__room
#
#     @room.setter
#     def room(self, room: np.zeros):
#         self.__room = room
#
#
# def main():
#     room = np.array([[1., 0., 1., 0., 0.],
#                      [0., 0., 0., 0., 0.],
#                      [1., np.nan, 1., np.nan, 1.],
#                      [np.nan, np.nan, np.nan, np.nan, np.nan]])
#
#     print(room)
#     tools = Tools(Prices(room, 1, 1))
#     print(f'{tools.prices.quarter_index=}')
#     print(f'{tools.prices.day_index=}')
#     print(f'{tools.prices.get_price=}')
#     tools = Tools(Prices(room, 0, 4))
#     print(f'{tools.prices.quarter_index=}')
#     print(f'{tools.prices.day_index=}')
#     print(f'{tools.prices.get_price=}')
#
#
# if __name__ == '__main__':
#     main()
