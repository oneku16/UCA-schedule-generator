from .instructors import Instructors
from .pattern import get_pattern


class Subject:
    __slots__ = ('__cohort', '__id', '__instructors', '__pattens', '__title')

    def __init__(self, *, cohort, id, instructor, patterns, title):
        self.__cohort = cohort
        self.__id = id
        self.__instructors = Instructors(**instructor)
        self.__pattens = get_pattern(patterns=patterns)
        self.__title = title

    @property
    def priority(self):
        instructor = int(self.__instructors.primary is not None) + int(self.__instructors.secondary is None)
        preferences = 0
        patterns = len(self.__pattens)
        return patterns, instructor, preferences

    @property
    def instructors(self):
        return self.__instructors

    @property
    def patterns(self):
        return self.__pattens

    @property
    def title(self):
        return self.__title

    @property
    def cohort(self):
        return self.__cohort