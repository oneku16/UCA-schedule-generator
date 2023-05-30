from typing import Tuple, List


class Instructor:
    ...


class Pattern:
    __slots__ = ('__classes', '__initial', '__duration', '__pattern')

    def __init__(self, pattern):
        self.__classes, self.__duration = pattern
        self.__initial = self.__classes

    @property
    def classes(self) -> int:
        return self.__classes

    @property
    def duration(self) -> int:
        return self.__duration

    def is_possible(self, back) -> bool:
        if back is None:
            return self.__classes >= 1
        return self.__classes + back <= self.__initial

    def reset_reservation(self, back: int = None):
        if back is None and self.is_possible(back):
            self.__classes -= 1
        if self.is_possible(back):
            self.__classes += back if back == 1 else 0
        raise f'out of initial value {self.__initial}'

    def reserve(self):
        ...


class Subject:
    __slots__ = ('__id', '__name', '__cohort', '__pattern', '__instructor')

    def __init__(self, subject_id: int | str,
                 subject_name: str,
                 cohort: str,
                 subject_pattern: Tuple[Tuple[int, int]],
                 instructor: dict):
        self.__id = subject_id
        self.__name = subject_name
        self.__cohort = cohort
        self.__pattern = subject_pattern
        self.__instructor = instructor
