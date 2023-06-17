from collections import deque
from genetic_deap_demo_1.subjects.subject import Subject


class Slots:
    __slots__ = ('__quarters', '__reserved', '__stack', '__size')

    def __init__(self):
        self.__quarters = {f'quarter{index}': {'status': True, 'subject': None} for index in (1, 2, 3, 4)}
        self.__size = 4
        self.__stack = deque()

    @property
    def is_full(self) -> bool:
        return self.__size == 0

    def __is_possible(self):
        ...

    def reserve_slot(self):
        ...


class Day:
    __slots__ = '_day_name'

    def __init__(self, day_name):

        self._day_name = day_name


