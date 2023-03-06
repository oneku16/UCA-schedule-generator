from typing import NamedTuple


class Subject:
    __slots__ = '_subject_id', '_subject_name', '_cohort', '_lecture', '_tutorial', '_laboratory', '_instructors'

    def __init__(self, subject_id, subject_name, cohort, subject_patterns, instructors):
        self._subject_id = subject_id
        self._subject_name = subject_name
        self._cohort = cohort
        self._instructors = instructors
        try:
            self._lecture, self._tutorial, self._laboratory = subject_patterns
        except ValueError:
            self._laboratory = None
            try:
                self._tutorial = None
                self._lecture, self._tutorial = subject_patterns
            except ValueError:
                self._lecture = subject_patterns

    @property
    def get_subject_id(self):
        return self._subject_id

    @property
    def get_subject_name(self):
        return self._subject_name

    @property
    def get_cohort(self):
        return self._cohort

    @property
    def get_lecture(self):
        return self._lecture

    @property
    def get_tutorial(self):
        return self._tutorial

    @property
    def get_laboratory(self):
        return self._laboratory

    def set_laboratory(self):
        pass
