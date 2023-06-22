from dataclasses import dataclass, field, InitVar
from typing import Dict


@dataclass(kw_only=True, slots=True)
class InstructorBuilder:
    instructor_id: str = field(repr=True, default=None)
    instructor_name: str = field(repr=True, default=None)
    preferences: dict = field(repr=True, default=None)


@dataclass(kw_only=True, slots=True)
class Instructors:
    primary: InstructorBuilder = InitVar[Dict]
    secondary: InstructorBuilder = None

    def __post_init__(self):
        self.primary = InstructorBuilder(**self.primary)
        if self.secondary:
            self.secondary = InstructorBuilder(**self.secondary)
