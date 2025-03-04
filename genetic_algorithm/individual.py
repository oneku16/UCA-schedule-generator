from random import choice

from constraints.slot import Slot
from constraints.instructor import Instructor
from constraints.subject import Subject
from constraints.room import Room


class Individual:
    __slots__ = (
        "__chromosomes",
        "fitness",
        "args",
        "kwargs",
    )
    def __init__(self, *args, **kwargs) -> None:
        self.__chromosomes = None
        self.fitness = object()
        self.args = args
        self.kwargs = kwargs

    @property
    def chromosomes(self) -> list[list[Subject, Slot, Room, Instructor]]:
        if self.__chromosomes is None:
            raise Exception("Build chromosomes first")
        return self.__chromosomes

    @chromosomes.setter
    def chromosomes(self, chromosomes: list[list[Subject, Slot, Room, Instructor]]) -> None:
        self.__chromosomes = chromosomes

    def build(
            self,
            subjects: list[Subject],
            instructors: list[Instructor],
            rooms: list[Room],
    ) -> None:
        self.__chromosomes = list()
        for subject in subjects:
            room = choice(rooms)
            slot = Slot(duration=subject.duration)
            slot.update_values()
            instructor = choice(instructors)
            gene = [
                subject,
                slot,
                room,
                instructor,
            ]
            self.__chromosomes.append(gene)
        self.fitness = object()
