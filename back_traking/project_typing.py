from typing import NamedTuple


class One:
    ...


class Two:
    ...


class Three:
    ...


class Four:
    ...


class Five:
    ...


class Subject:

    __slots__ = '_subject_id', '_subject_name', '_cohort', '_subject_patterns', '_lecture', '_tutorial', '_laboratory', '_instructors'

    def __init__(self, subject_id, subject_name, cohort, subject_patterns, instructors):
        self._subject_id = subject_id
        self._subject_name = subject_name
        self._cohort = cohort
        self._instructors = instructors
        self._subject_patterns = subject_patterns
        # for _, patterns in zip((self._lecture, self._tutorial, self._laboratory), subject_patterns):
        #     _ = patterns

    def get_subject_id(self):
        return self._subject_id

    def get_subject_name(self):
        return self._subject_name

    def get_cohort(self):
        return self._cohort

    def get_subject_patterns(self):
        return self._subject_patterns
        # return self._lecture, self._tutorial, self._laboratory




