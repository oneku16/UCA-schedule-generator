from typing import List, Tuple, Type


class Subject:
    __slots__ = '__subject_id', '__subject_name', '__subject_cohort', '__subject_pattern', '__subject_instructor'

    def __init__(self, subject_id, subject_name, subject_cohort, subject_pattern, subject_instructor):
        self.__subject_id = subject_id
        self.__subject_name = subject_name
        self.__subject_cohort = subject_cohort
        self.__subject_pattern = subject_pattern
        self.__subject_instructor = subject_instructor

    @property
    def subject_id(self):
        return self.__subject_id

    @property
    def subject_name(self):
        return self.__subject_name

    @property
    def subject_cohort(self):
        return self.__subject_cohort

    @property
    def subject_pattern(self):
        return self.__subject_pattern

    @property
    def subject_instructor(self):
        return self.__subject_instructor

    def __repr__(self):
        return f'id: {self.__subject_id}, name: {self.__subject_name}, cohort: {self.__subject_cohort}, ' \
               f'pattern: {self.__subject_pattern}, instructor: {self.__subject_instructor}'
