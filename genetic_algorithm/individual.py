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
        "__room_map"
    )
    def __init__(self, rooms: list[Room]):
        self.__rooms: defaultdict[str, list[Room]] = self.build_room_structure(rooms)

    @property
    def rooms(self):
        return self.__rooms

    @staticmethod
    def build_room_structure(
            rooms: list[Room],
    ) -> defaultdict[str, list[Room]]:
        mapped = defaultdict(list)

        for room in rooms:
            mapped[room.room_type].append([20, room])
        return mapped

    def __update_room(self, room_type: str, index: int) -> Room:
        rooms = self.__rooms[room_type]
        rooms[index], rooms[-1] = rooms[-1], rooms[index]
        count, room = rooms.pop()
        count -= 1
        rooms.append([count, room])

        if count == 0:
            rooms.pop()
        return room

    def reduce_room(self, room: Room) -> None:
        index = 0

        while index < len(self.__rooms[room.room_type]):
            if room.room_id == self.__rooms[room.room_type][index][1].room_id:
                self.__rooms[room.room_type][index][0] -= 1
                if self.__rooms[room.room_type][index][0] == 0:
                    continue
            index += 1

    def put_room(self, room: Room) -> None:
        for index in range(len(self.__rooms[room.room_type])):
            if self.__rooms[room.room_type][index][1].room_id == room.room_id:
                self.__rooms[room.room_type][index][0] += 1
                return
        self.__rooms[room.room_type].append([1, room])

    def get_room(self, room_types: frozenset[str]) -> Room:

        room_types = tuple([r for r in room_types if r != 'tutorial'])

        if all(not self.__rooms[rt] for rt in room_types):
            room_types = tuple(self.__rooms.keys())

        while room_type := choice(room_types):
            if self.__rooms[room_type]:
                break

        index = randint(0, len(self.__rooms[room_type]) - 1)
        room = self.__update_room(room_type, index)

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
