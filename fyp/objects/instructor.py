from datetime import datetime

from .mixin import PersonMixin


class Instructor(PersonMixin):

    def __init__(self, first_name: str, last_name: str, email: str, instructor_id: str,
                 start_time: str, end_time: str, cohorts: frozenset[str], courses: dict[str, str],
                 ):
        super().__init__(first_name, last_name, email)
        self.instructor_id = instructor_id
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.end_time = datetime.strptime(end_time, '%H:%M')
        self.cohorts = cohorts
        self.courses = courses

    def is_my_cohort(self, cohort_id: str) -> bool:
        """
        :return: True if cohort is in instructor's course list, otherwise False
        """
        return cohort_id in self.cohorts

    def is_my_course(self, subject_id: str) -> bool:
        """
        :return: True if subject is in instructor's course list, otherwise False
        """
        return subject_id in self.courses

    def is_my_time(self, start_time: str, end_time: str) -> bool:
        """
        :return: True if start_time and end_time fit instructor's time, otherwise False
        """
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        return self.start_time <= start_time < end_time <= self.end_time

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'
