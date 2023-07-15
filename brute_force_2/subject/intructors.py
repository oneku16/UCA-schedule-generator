from dataclasses import dataclass, field, InitVar


@dataclass(kw_only=True, slots=True)
class InstructorBuilder:
    instructor_id: str = field(repr=True, default=None)
    instructor_name: str = field(repr=True, default=None)
    preferences: dict = field(repr=True, default=None)


@dataclass(kw_only=True)
class Instructors:
    primary: InitVar[InstructorBuilder]
    secondary: InitVar[InstructorBuilder] = None

    def __post_init__(self, primary, secondary):
        self.primary = InstructorBuilder(**primary)
        self.secondary = secondary and InstructorBuilder(**secondary)