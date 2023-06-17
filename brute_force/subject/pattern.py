from config import SUBJECT_PATTERNS
from typing import Tuple, List


class Pattern:
    __slots__ = ('__subject_type', '__classes', '__duration', '__required_rooms', '__priority')

    def __init__(self, *, subject_type: str, pattern: Tuple[int, int]):
        self.__subject_type = subject_type
        self.__classes, self.__duration = pattern
        self.__required_rooms = list()
        self.__priority = len(pattern)

    def __str__(self):
        return f'{self.__subject_type} {self.__classes} {self.__duration}'

    @property
    def subject_type(self):
        return self.__subject_type

    @property
    def priority(self):
        return self.__priority


def get_pattern(*, patterns: Tuple[Tuple[int, int]]) -> List[Pattern]:

    return [Pattern(subject_type=subject_type, pattern=pattern) for subject_type, pattern in zip(SUBJECT_PATTERNS, patterns)]

