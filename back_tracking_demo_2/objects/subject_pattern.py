from typing import Tuple, List
from back_tracking_demo_2.configs import SUBJECT_PATTERNS


class SubjectPattern:
    __slots__ = '__patterns'

    def __init__(self, patterns: Tuple[Tuple[int, int]]):
        self.__patterns = self.__make_pattern(patterns)

    def __iter__(self):
        for pattern in self.__patterns:
            yield pattern

    def __len__(self):
        return len(self.__patterns)

    @property
    def patterns(self):
        return self.__patterns

    @classmethod
    def __make_pattern(cls, patterns: Tuple[Tuple[int, int]]) -> List[int]:
        return []
