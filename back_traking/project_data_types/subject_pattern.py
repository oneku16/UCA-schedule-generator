from .subject_pattern_type import SubjectPatternType
from back_traking.configs import SUBJECT_PATTERNS


class SubjectPattern:
    __slots__ = '_patterns', '_counter'

    def __init__(self, patterns):
        self._patterns = list(self.__get_subject_patterns(patterns))
        self._counter = len(patterns)

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
    def __get_subject_patterns(cls, patterns) -> list:
        for _type, _pattern in zip(SUBJECT_PATTERNS, patterns):
            yield SubjectPatternType(name=_type, pattern=_pattern)
