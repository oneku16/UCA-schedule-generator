from .subject_pattern import SubjectPattern
from .intructor import Instructor


class Subject:
    __slots__ = '_subject_id', '_subject_name', '_cohort', '_subject_pattern', '_instructor'

    def __init__(self, subject_id, subject_name, cohort, subject_pattern, instructor):
        self._subject_id = subject_id
        self._subject_name = subject_name
        self._cohort = cohort
        self._subject_pattern = SubjectPattern(subject_pattern)
        self._instructor = Instructor(**instructor)

    def __str__(self):
        return f'{self._subject_id}-{self._subject_name}'

    @property
    def subject_id(self):
        return self._subject_id

    @property
    def subject_name(self):
        return self._subject_name

    @property
    def cohort(self):
        return self._cohort

    @property
    def subject_pattern(self):
        return self._subject_pattern

    @property
    def instructor(self):
        return self._instructor

    @property
    def full_information(self):
        return f'id={self._subject_id}, title={self._subject_name}, pattern={[(pattern.name, pattern.number_of_classes) for pattern in self._subject_pattern.patterns]}'
