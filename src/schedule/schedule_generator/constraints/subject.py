from typing import Any, Optional


class Subject:
    """
    Represents a subject with its ID, name, cohort, duration, preferred rooms, and requirements.
    Attributes:
        subject_id (str): A unique identifier for the subject.
        subject_name (str): The name of the subject.
        cohort (str): The cohort associated with the subject.
        duration (int): The duration of the subject in minutes.
        preferred_rooms (frozenset[str]): A set of preferred rooms for the subject.
        requirements (MappingProxyType): A read-only dictionary of requirements for the subject.
        optional_requirements (MappingProxyType): A read-only dictionary of optional requirements for the subject.
        is_required (bool): Indicates whether the subject is required. Defaults to False.
    """
    __slots__ = (
        "subject_id",
        "subject_name",
        "cohort",
        "duration",
        "preferred_rooms",
        "requirements",
        "optional_requirements",
        "is_required",
    )

    def __init__(
            self,
            subject_id: str,
            subject_name: str,
            cohort: str,
            duration: int,
            preferred_rooms: Optional[list[str]] = None,
            requirements: Optional[dict[str, Any]] = None,
            optional_requirements: Optional[dict[str, Any]] = None,
            is_required: Optional[bool] = False,
    ):
        """
        Initializes a Subject instance.
        Args:
            subject_id (str): A unique identifier for the subject.
            subject_name (str): The name of the subject.
            cohort (str): The cohort associated with the subject.
            duration (int): The duration of the subject in minutes.
            preferred_rooms (Optional[list[str]]): A list of preferred rooms for the subject. Defaults to None.
            requirements (dict[str, Any]): A dictionary of requirements for the subject. Should not be modified after initialization.
            optional_requirements (dict[str, Any]): A dictionary of optional requirements for the subject. Should not be modified after initialization.
            is_required (bool): Indicates whether the subject is required. Defaults to False.
        Raises:
            ValueError: If `subject_id`, `subject_name`, or `cohort` is empty, or if `duration` is not a positive integer.
        """
        if not isinstance(subject_id, str) or not subject_id:
            raise ValueError("subject_id must be a non-empty string")
        if not isinstance(subject_name, str) or not subject_name:
            raise ValueError("subject_name must be a non-empty string")
        if not isinstance(cohort, str) or not cohort:
            raise ValueError("cohort must be a non-empty string")
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("duration must be a positive integer")

        self.subject_id = subject_id
        self.subject_name = subject_name
        self.cohort = cohort
        self.duration = duration
        self.preferred_rooms = frozenset(preferred_rooms) if preferred_rooms else frozenset()
        self.requirements = requirements or {}
        self.optional_requirements = optional_requirements or {}
        self.is_required = is_required

    @property
    def subject_full_id(self) -> str:
        """
        Returns a unique identifier for the subject, combining `subject_id` and `cohort`.
        Returns:
            str: The full subject ID.
        """
        return f"{self.subject_id}-{self.cohort}"

    def __eq__(self, other):
        """
        Checks if two Subject instances are equal based on their `subject_full_id`.
        Args:
            other (Any): The object to compare with.
        Returns:
            bool: True if the objects are equal, otherwise False.
        """
        if not isinstance(other, Subject):
            return False
        return self.subject_full_id == other.subject_full_id

    def __hash__(self):
        """
        Returns a hash value for the Subject instance based on its `subject_full_id`.
        Returns:
            int: The hash value.
        """
        return hash(self.subject_full_id)

    def __repr__(self) -> str:
        return f'Subject(id={self.subject_id}, name={self.subject_name}, rooms={self.preferred_rooms})'