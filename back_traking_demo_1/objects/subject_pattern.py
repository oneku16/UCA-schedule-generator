from .subject_pattern_type import SubjectPatternType
from back_traking_demo_1.configs import SUBJECT_PATTERNS
from typing import List, Tuple


class SubjectPattern:
    __slots__ = '_patterns', '_counter'

    def __init__(self, patterns: Tuple[Tuple[int, int]]):
        self._patterns = self.__get_subject_patterns(patterns)
        self._counter = len(patterns)

    def __iter__(self):
        for pattern in self._patterns:
            yield pattern

    @property
    def counter(self):
        """
        returns number of patterns
        """
        return self._counter

    @property
    def patterns(self):
        """
        returns a list of SubjectPatterns, which stores links to pattern objects
        """
        return self._patterns

    @classmethod
    def __get_subject_patterns(cls, patterns) -> List[SubjectPatternType]:
        def _wrapper():
            for _type, _pattern in zip(SUBJECT_PATTERNS, patterns):
                yield SubjectPatternType(name=_type, pattern=_pattern)
        return list(_wrapper())

    def previous(self):
        ...
