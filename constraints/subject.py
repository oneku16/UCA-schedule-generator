from typing import Any, Optional


class Subject:
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
        self.subject_id: str = subject_id
        self.subject_name: str = subject_name
        self.cohort: str = cohort
        self.duration: int = duration
        self.preferred_rooms: frozenset[str] = frozenset(preferred_rooms) if preferred_rooms else frozenset()
        self.requirements: dict[str, Any] = requirements if requirements else dict()
        self.optional_requirements: dict[str, Any] = optional_requirements if optional_requirements else dict()
        self.is_required = is_required

    @property
    def subject_full_id(self) -> str:
        return f"{self.subject_id}-{self.cohort}"

    def __repr__(self):
        return f'Subject(id={self.subject_id}, name={self.subject_name}, rooms={self.preferred_rooms})'
