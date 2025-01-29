from datetime import time
from typing import Optional


class Instructor:

    def __init__(
            self,
            first_name: str,
            last_name: str,
            email: Optional[str] = None,
            instructor_id: Optional[str] = None,
            cohorts: Optional[frozenset[str]] = None,
            courses: Optional[frozenset[str]] = None,
            start_time: Optional[str | time] = None,
            end_time: Optional[str | time] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.instructor_id = instructor_id
        self.cohorts = cohorts or frozenset()
        self.courses = courses or frozenset()
        self.start_time = time.fromisoformat(start_time) if isinstance(start_time, str) else None
        self.end_time = time.fromisoformat(end_time) if isinstance(end_time, str) else None

    def is_my_cohort(self, cohort_id: str) -> bool:
        """
        :return: True if cohort is in instructor's course list, otherwise False
        """
        assert isinstance(cohort_id, str)
        return cohort_id in self.cohorts

    def is_my_course(self, subject_id: str) -> bool:
        """
        :return: True if subject is in instructor's course list, otherwise False
        """
        assert isinstance(subject_id, str)
        return subject_id in self.courses

    def is_my_time(self, other_start_time: str | time, other_end_time: str | time) -> bool:
        if self.start_time is None or other_start_time is None:
            return True
        """
        :return: True if start_time and end_time fit instructor's time, otherwise False
        """
        assert isinstance(other_start_time, (str, time))
        assert isinstance(other_end_time, (str, time))
        other_start_time = time.fromisoformat(other_start_time) if isinstance(other_start_time, str) else other_start_time
        other_end_time = time.fromisoformat(other_end_time) if isinstance(other_end_time, str) else other_end_time
        assert other_start_time < other_end_time
        return self.start_time <= other_start_time and other_end_time <= self.end_time
