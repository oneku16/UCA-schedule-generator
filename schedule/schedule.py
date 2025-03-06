from collections import defaultdict
from typing import Optional, Generator, TypeVar

from config import DAYS, SLOTS

from constraints.subject import Subject
from constraints.slot import Slot
from constraints.instructor import Instructor
from constraints.room import Room
from data_structures.dictionaries import ScheduleDictionary


slots: tuple[str, ...] = tuple(
        f"{slot['hour']}:{slot['minute']}" for slot in SLOTS
    )


NodeType = TypeVar('NodeType', bound='Node')


class Node:
    __slots__ = (
        "name",
        "prev_node",
        "next_node",
    )
    def __init__(
            self,
            name: Optional[str] = None,
            prev_node: Optional[NodeType] = None,
            next_node: Optional[NodeType] = None,
    ) -> None:
        self.name = name
        self.prev_node = prev_node
        self.next_node = next_node

    def set_values(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class NodeSlot(Node):
    __slots__ = Node.__slots__ + (
        "subject",
        "room",
        "slot",
        "instructor",
        "collected"
    )
    def __init__(
            self,
            name: Optional[str] = None,
            subject: Optional[Subject] = None,
            room: Optional[Room] = None,
            slot: Optional[Slot] = None,
            instructor: Optional[Instructor] = None,
    ) -> None:
        super().__init__(name=name)
        self.subject = subject
        self.room = room
        self.slot = slot
        self.instructor = instructor

    def is_empty(self) -> bool:
        return self.subject is None

    def get_data(self) -> tuple[Subject, Slot, Room, Instructor]:
        return self.subject, self.slot, self.room, self.instructor

    def set_values(
            self,
            *,
            subject: Optional[Subject] = None,
            slot: Optional[Slot] = None,
            room: Optional[Room] = None,
            instructor: Optional[Instructor] = None,
    ) -> None:
        if self.is_empty():
            self.subject = subject
            self.room = room
            self.slot = slot
            self.instructor = instructor

    def __repr__(self) -> str:
        return f'NodeSlot(name={self.name}, subject={self.subject}, room={self.room}, slot={self.slot}, instructor={self.instructor})'


class NodeDay(Node):
    __slots__ = Node.__slots__ + (
        "slot",
    )
    def __init__(self, name: str, slot: Optional['Slots'] = None) -> None:
        super().__init__(name)
        self.slot = slot

    def set_values(self, slot: 'Slots') -> None:
        self.slot = slot

    def __repr__(self) -> str:
        return f'NodeDay(day={self.name}, slot={self.slot})'

    def __getitem__(self, start_time: str):
        return self.slot[start_time]


class LinkedListMapBase:
    __slots__ = (
        "head",
        "tail",
        "pointer",
        "map"
    )
    def __init__(self):
        self.head: Node = Node(None)
        self.tail: Node = Node(None)
        self.head.next_node = self.tail
        self.tail.prev_node = self.head
        self.map = dict()
        self.pointer: Optional[Node] = None

    def backward(self) -> Node | None:
        if self.pointer is self.head.next_node:
            return None
        self.pointer = self.pointer.prev_node
        return self.pointer

    def forward(self) -> Node | None:
        if self.pointer is self.tail.prev_node:
            return None
        self.pointer = self.pointer.next_node
        return self.pointer

    def pointer_iter(self) -> Generator[Node, None, None]:
        self.pointer = self.head.next_node

        while self.pointer != self.tail:
            yield self.pointer
            self.pointer = self.pointer.next_node

        self.pointer = self.head.next_node


class Slots(LinkedListMapBase):
    def __init__(self) -> None:
        super().__init__()
        self.pointer: NodeSlot
        for start_time in slots:
            node = NodeSlot(start_time)
            self.map[start_time] = node
            node.prev_node = self.tail.prev_node
            node.next_node = self.tail
            self.tail.prev_node.next_node = node
            self.tail.prev_node = node

        self.pointer: NodeSlot = self.head.next_node

    def is_full(self) -> bool:
        for node_slot in self.map.values():
            if node_slot.is_empty():
                return False
        return True

    def is_overfitted(self) -> bool:
        for node_slot in self.map.values():
            if len(node_slot.collected) >= 2:
                return False
        return True

    def get_schedule(self) -> ScheduleDictionary:
        schedule_dictionary = ScheduleDictionary()
        curr = self.head.next_node
        while curr != self.tail:
            if not curr.is_empty():
                schedule_dictionary[curr.subject.subject_full_id].append(curr.get_data())
            curr = curr.next_node

        return schedule_dictionary

    def pointer_iter(self) -> Generator[NodeSlot, None, None]:
        self.pointer = self.head.next_node
        while self.pointer != self.tail:
            yield self.pointer
            self.pointer = self.pointer.next_node
        self.pointer = self.head.next_node

    def __iter__(self) -> Generator[tuple[Subject, Slot, Room, Instructor], None, None]:

        dummy: NodeSlot = self.head.next_node
        while dummy != self.tail:
            yield dummy.subject, dummy.slot, dummy.room, dummy.instructor,

            dummy = dummy.next_node

    def __getitem__(self, start_time) -> NodeSlot:
        return self.map[start_time]

    def __repr__(self) -> str:
        return f'Slots({", ".join(map(str, self.map.items()))})'


class Day(LinkedListMapBase):
    def __init__(self) -> None:
        super().__init__()

        for week_day in DAYS:
            node = NodeDay(week_day)
            node.slot = Slots()
            self.map[week_day] = node
            node.prev_node = self.tail.prev_node
            node.next_node = self.tail
            self.tail.prev_node.next_node = node
            self.tail.prev_node = node

        self.pointer: NodeDay = self.head.next_node

    def get_schedule(self) -> ScheduleDictionary:
        schedule_dictionary = ScheduleDictionary()
        curr_day = self.head.next_node

        while curr_day != self.tail:
            if not curr_day.is_empty():
                curr_slot = curr_day.head.next_node
                while curr_slot != curr_day.tail:
                    if not curr_slot.is_empty():
                        schedule_dictionary[curr_slot.subject.subject_full_id].append(curr_slot.get_data())
                    curr_slot = curr_slot.next_node
            curr_day = curr_day.next_node

        return schedule_dictionary

    def pointer_iter(self) -> Generator[NodeDay, None, None]:
        self.pointer = self.head.next_node
        while self.pointer != self.tail:
            yield self.pointer
            self.pointer = self.pointer.next_node
        self.pointer = self.head.next_node

    def __iter__(self) -> Generator[Slots, None, None]:

        dummy: NodeDay = self.head.next_node
        while dummy != self.tail:
            yield dummy.slot
            dummy = dummy.next_node

    def __getitem__(self, week_day) -> Slots:
        return self.map[week_day]


class Schedule:
    __slots__ = (
        "__room_map",
        "__subject_map"
    )
    def __init__(self, rooms: list[Room]):
        self.__room_map: dict[str, Day] = {
            room.room_id: Day() for room in rooms
        }
        self.__subject_map: defaultdict[str, list[Slot]] = defaultdict(list)

    def assign_event(
            self,
            *,
            subject: Subject,
            slot: Slot,
            room: Room,
            instructor: Optional[Instructor] = None,
    ) -> bool:
        target_slot = self.__room_map[room.room_id][slot.week_day][slot.start_time]
        if not target_slot.is_empty():
            return False
        target_slot.set_values(subject=subject, room=room, slot=slot, instructor=instructor)
        self.__subject_map[subject.subject_full_id].append(slot)
        return True

    @property
    def room_map(self):
        return self.__room_map

    @property
    def subject_map(self):
        return self.__subject_map

    def get_room_schedule(self, room: Room) -> Day:
        return self.__room_map[room.room_id]

    def get_rooms_schedule(self) -> list[Day]:
        days = list(self.__room_map.values())
        return days

    def get_slots_in_room(self, room: Room, slot: Slot) -> Slots:
        return self.__room_map[room.room_id][slot.week_day]

    def __iter__(self) -> Generator[tuple[str, Day], None, None]:
        for room_id, day in self.__room_map.items():
            yield room_id, day
