from datetime import time
from typing import Optional


class Instructor:
    """
    Represents an instructor with their personal details, assigned cohorts, courses, and working hours.

    Attributes:
        first_name (str): The first name of the instructor.
        last_name (str): The last name of the instructor.
        email (Optional[str]): The email address of the instructor. Defaults to None.
        instructor_id (Optional[str]): A unique identifier for the instructor. Defaults to None.
        cohorts (frozenset[str]): A set of cohort IDs assigned to the instructor. Defaults to an empty frozenset.
        courses (frozenset[str]): A set of course IDs assigned to the instructor. Defaults to an empty frozenset.
        start_time (Optional[time]): The start time of the instructor's working hours. Defaults to None.
        end_time (Optional[time]): The end time of the instructor's working hours. Defaults to None.
    """

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
        """
        Initializes an Instructor instance.

        Args:
            first_name (str): The first name of the instructor.
            last_name (str): The last name of the instructor.
            email (Optional[str]): The email address of the instructor. Defaults to None.
            instructor_id (Optional[str]): A unique identifier for the instructor. Defaults to None.
            cohorts (Optional[frozenset[str]]): A set of cohort IDs assigned to the instructor. Defaults to None.
            courses (Optional[frozenset[str]]): A set of course IDs assigned to the instructor. Defaults to None.
            start_time (Optional[str | time]): The start time of the instructor's working hours. Can be a string in ISO format
                                              or a `datetime.time` object. Defaults to None.
            end_time (Optional[str | time]): The end time of the instructor's working hours. Can be a string in ISO format
                                            or a `datetime.time` object. Defaults to None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.instructor_id = instructor_id
        self.cohorts = cohorts or frozenset()
        self.courses = courses or frozenset()
        self.start_time = time.fromisoformat(start_time) if isinstance(start_time, str) else start_time
        self.end_time = time.fromisoformat(end_time) if isinstance(end_time, str) else end_time

    def is_my_cohort(self, cohort_id: str) -> bool:
        """
        Checks if a given cohort ID is assigned to the instructor.

        Args:
            cohort_id (str): The cohort ID to check.

        Returns:
            bool: True if the cohort ID is in the instructor's assigned cohorts, otherwise False.

        Raises:
            TypeError: If `cohort_id` is not a string.
        """
        if not isinstance(cohort_id, str):
            raise TypeError("cohort_id must be a string")
        return cohort_id in self.cohorts

    def is_my_course(self, subject_id: str) -> bool:
        """
        Checks if a given course ID is assigned to the instructor.

        Args:
            subject_id (str): The course ID to check.

        Returns:
            bool: True if the course ID is in the instructor's assigned courses, otherwise False.

        Raises:
            TypeError: If `subject_id` is not a string.
        """
        if not isinstance(subject_id, str):
            raise TypeError("subject_id must be a string")
        return subject_id in self.courses

    def is_my_time(self, other_start_time: str | time, other_end_time: str | time) -> bool:
        """
        Checks if a given time range fits within the instructor's working hours.

        Args:
            other_start_time (str | time): The start time of the range to check. Can be a string in ISO format
                                          or a `datetime.time` object.
            other_end_time (str | time): The end time of the range to check. Can be a string in ISO format
                                        or a `datetime.time` object.

        Returns:
            bool: True if the time range fits within the instructor's working hours, otherwise False.
                  Returns True if the instructor's working hours are not set (i.e., `start_time` or `end_time` is None).

        Raises:
            TypeError: If `other_start_time` or `other_end_time` is not a string or `datetime.time` object.
            ValueError: If `other_start_time` is not less than `other_end_time`.
        """
        if self.start_time is None or self.end_time is None:
            return True

        if not isinstance(other_start_time, (str, time)):
            raise TypeError("other_start_time must be a string or datetime.time object")
        if not isinstance(other_end_time, (str, time)):
            raise TypeError("other_end_time must be a string or datetime.time object")

        try:
            other_start_time = time.fromisoformat(other_start_time) if isinstance(other_start_time, str) else other_start_time
            other_end_time = time.fromisoformat(other_end_time) if isinstance(other_end_time, str) else other_end_time
        except ValueError as e:
            raise ValueError(f"Invalid time format: {e}")

        if other_start_time >= other_end_time:
            raise ValueError("other_start_time must be less than other_end_time")

        return self.start_time <= other_start_time and other_end_time <= self.end_time

    def __repr__(self):
        return (f"Instructor(first_name={self.first_name}, last_name={self.last_name}, "
                f"email={self.email}, instructor_id={self.instructor_id})")
