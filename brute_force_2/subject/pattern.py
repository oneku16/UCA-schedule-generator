from dataclasses import dataclass, field
from typing import Any, Iterable, List, Dict
from config import SUBJECT_PATTERNS


@dataclass(kw_only=True)
class Pattern:
    subject_type: str
    classes: int
    duration: int
    required_rooms: List[Any] = field(init=False, default_factory=set)

    def add_rooms(self, *args: Iterable[object]) -> None:
        self.required_rooms.extend(args)


def get_pattern(*, patterns: List[Dict[str, int]]) -> List[Pattern]:
    return list(Pattern(subject_type=subject_type, **pattern) for subject_type, pattern in zip(SUBJECT_PATTERNS, patterns))
