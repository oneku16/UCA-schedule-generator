from typing import Tuple, List
from dataclasses import dataclass, Field


@dataclass
class Pattern:
    classes: int
    duration: int
    initial: int = Field(init=False)

    def __post_init__(self):
        self.initial = self.classes





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
