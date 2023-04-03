from typing import List, Tuple
from dataclasses import dataclass, InitVar, field


@dataclass(order=True)
class Class:
    number_of_classes: int
    class_duration: int
    initial_number_of_classes: int = field(init=False)

    def __post_init__(self):
        self.initial_number_of_classes = self.class_duration


class Lecture(Class):
    rooms = []
    ...


class Laboratory(Class):
    ...


