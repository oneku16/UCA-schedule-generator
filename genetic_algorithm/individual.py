from collections import defaultdict
from random import choice, randint
from heapq import heappush, heappop

from constraints.slot import Slot
from constraints.instructor import Instructor
from constraints.subject import Subject
from constraints.room import Room


class RoomSelector:
    __slots__ = (
        "__rooms",
    )
    def __init__(self, rooms: list[Room]):
        self.__rooms = self.build_room_structure(rooms)

    @staticmethod
    def build_room_structure(rooms: list[Room]) -> defaultdict[str, list[Room]]:
        mapped = defaultdict(list)

        for room in rooms:
            mapped[room.room_type].append((20, room))
        return mapped

    def get_room(self, room_types: frozenset[str]) -> Room:

        room_types = tuple([r for r in room_types if r != 'tutorial'])
        room_type = choice(room_types)

        if not self.__rooms[room_type]:
            keys = list(self.__rooms.keys())
            if len(room_types) == 1:
                while new_room_type := choice(keys):
                    if new_room_type != room_type and self.__rooms[new_room_type]:
                        room_type = new_room_type
                        break
            else:
                while new_room_type := choice(room_types):
                    if new_room_type != room_type and self.__rooms[new_room_type]:
                        room_type = new_room_type
                        break

        index = randint(0, len(self.__rooms[room_type]) - 1)
        rooms = self.__rooms[room_type]
        rooms[index], rooms[-1] = rooms[-1], rooms[index]
        count, room = rooms.pop(index)
        if count - 1 >= 0:
            rooms.append((count - 1, room))
        return room


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
