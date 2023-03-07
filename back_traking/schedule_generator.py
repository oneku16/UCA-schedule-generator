from functools import reduce
from typing import Iterable, List, Literal
import numpy


class ScheduleGenerator:
    __slots__ = '_subjects'

    def __init__(self, subjects):
        self._subjects = subjects

    @property
    def get_all_subjects(self):
        return self._subjects
