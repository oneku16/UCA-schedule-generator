from dataclasses import dataclass, InitVar, field


@dataclass(kw_only=True, order=True)
class SubjectStructure:
    number_of_lessons: int
    lesson_duration: int
    initial_number_of_lessons: int = field(init=False)

    def __post_init__(self):
        self.initial_number_of_lessons = self.number_of_lessons

    ...


class Lecture(SubjectStructure):

    def __init__(self):
        self.rooms = (RoomLecture)
        super().__init__()


class Tutorial(SubjectStructure):
    ...


class Laboratory(SubjectStructure):
    ...

