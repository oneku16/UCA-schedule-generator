from typing import Optional


class Subject:
    def __init__(
            self,
            subject_id: str,
            subject_name: str,
            cohort: str,
            preferred_rooms: list[str],
            requirements: Optional[dict] = None,
            optional_requirements: Optional[dict] = None,
            is_required: bool = False,
    ):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.cohort = cohort
        self.preferred_rooms = frozenset(preferred_rooms)
        self.requirements = requirements
        self.optional_requirements = optional_requirements
        self.is_required = is_required

    @property
    def subject_full_id(self) -> str:
        return f"{self.subject_id}-{self.cohort}"

    def __repr__(self):
        return f'Subject(id={self.subject_id}, name={self.subject_name}, rooms={self.preferred_rooms})'
