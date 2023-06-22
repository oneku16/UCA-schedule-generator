from dataclasses import dataclass, InitVar
from typing import List, Dict
from .intructors import Instructors
from .pattern import get_pattern, Pattern


@dataclass(kw_only=True)
class Subject:
    cohort: str
    id: str | int
    title: str
    instructors: InitVar[Instructors]
    patterns: InitVar[List[Pattern]]

    def __post_init__(self, instructors: Dict, patterns: List[Dict[str, int]]):
        self.instructors: Instructors = Instructors(**instructors)
        self.patterns: List[Pattern] = get_pattern(patterns=patterns)

    @property
    def priority(self):
        instructor = int(self.instructors.primary is not None) + int(self.instructors.secondary is not None)
        preferences = 0
        patterns = len(self.patterns)
        return instructor, preferences, patterns
