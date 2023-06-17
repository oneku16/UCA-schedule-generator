from typing import Tuple, List
from genetic_deap_demo_1.settings import PATTERN_TYPE
from genetic_deap_demo_1.types.subject_types import get_subject_type


class Instructor:
    __slots__ = ('__primary', '__secondary', '_InstructorBuilder', '__priority')

    class __InstructorBuilder:
        __slots__ = ('__id', '__name', '__preferences')

        def __init__(self, instructor_id, instructor_name, preferences):
            self.__id = instructor_id
            self.__name = instructor_name
            self.__preferences = preferences

        @property
        def id(self):
            return self.__id

        @property
        def name(self):
            return self.__name

        @property
        def preferences(self):
            return self.__preferences

    def __init__(self, primary=None, secondary=None):
        self.__primary = primary
        self.__secondary = secondary
        self.__priority = int(primary is not None) + int(secondary is not None)

    @property
    def primary(self):
        return self.__primary

    @property
    def secondary(self):
        return self.__secondary

    @property
    def priority(self):
        return self.__priority


class Pattern:
    __slots__ = ('__classes', '__duration', '__initial', '__subject_type')

    def __init__(self, classes: int, duration: int, subject_type: object):
        self.__classes = self.__initial = classes
        self.__duration = duration
        self.__subject_type = subject_type

    @property
    def classes(self) -> int:
        return self.__classes

    @property
    def duration(self):
        return self.__duration

    @property
    def subject_type(self):
        return type(self.__subject_type)

    @classes.setter
    def classes(self, amount: int):
        self.__classes += amount

    def is_possible(self, amount: int) -> bool:
        assert amount in (-2, -1, 1, 2)
        if amount >= 1:  # case to check can we return back class
            return self.__classes + amount <= self.__initial
        else:  # case to check can we get class and reserve it
            return self.__classes + amount >= 0

    def reserve(self, number) -> None:
        if self.is_possible(number):
            self.__classes += number
        else:
            raise 'Wrong number of classes'

    def reset_reservation(self, number):
        if self.is_possible(number):
            self.__classes += number
        else:
            raise 'Wrong number of classes'


class Subject:
    __slots__ = ('__id', '__title', '__cohort', '__patterns', '__instructors')

    def __init__(self, id: int | str,
                 title: str,
                 cohort: str,
                 patterns: Tuple[Tuple[int, int]],
                 instructor: dict):
        self.__id = id
        self.__title = title
        self.__cohort = cohort
        self.__patterns = list(self.__generate_pattern(patterns))
        self.__instructors = Instructor(**instructor)

    @property
    def id(self) -> int | str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def cohort(self) -> str:
        return self.__cohort

    @property
    def patterns(self) -> List[Pattern]:
        return self.__patterns

    @property
    def instructors(self):
        return self.__instructors

    @classmethod
    def __generate_pattern(cls, *args):
        for (classes, duration), subject_type in zip(*args, PATTERN_TYPE):
            yield Pattern(classes=classes, duration=duration, subject_type=get_subject_type(subject_type))
