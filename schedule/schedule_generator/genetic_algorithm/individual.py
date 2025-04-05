from random import choice

from schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor
from schedule.schedule_generator.data_structures import RoomSelector


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
        room_selector = RoomSelector(rooms)
        self.__chromosomes = list()
        for subject in subjects:
            room = room_selector.get_room(subject.preferred_rooms)
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
