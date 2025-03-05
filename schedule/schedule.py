from typing import Optional, Generator

from config import DAYS, SLOTS

from constraints.subject import Subject
from constraints.slot import Slot
from constraints.instructor import Instructor
from constraints.room import Room


slots: tuple[str, ...] = tuple(
        f"{slot['hour']}:{slot['minute']}" for slot in SLOTS
    )


class Node:
    __slots__ = (
        "name",
        "prev_node",
        "next_node",
    )
    def __init__(
            self,
            name: str,
            prev_node: Optional['Node'] = None,
            next_node: Optional['Node'] = None,
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
            name: str,
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
        self.collected: list[tuple[Subject, Slot, Room, Instructor]] = list()

    def is_empty(self) -> bool:
        return self.subject is None

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
        self.collected.append((subject, slot, room, instructor))

    def __repr__(self) -> str:
        return f'NodeSlot(name={self.name}, subject={self.subject}, room={self.room}, slot={self.slot}, instructor={self.instructor})'


class NodeDay(Node):
    __slots__ = Node.__slots__ + (
        "slot",
    )
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.slot: Optional['Slots'] = None

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
        self.head: Node = Node('_Head')
        self.tail: Node = Node('_Tail')
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

        self.pointer = self.head.next_node

    def is_full(self) -> bool:
        for node_slot in self.map.values():
            if node_slot.is_empty():
                return False
        return True

    def is_overfitted(self) -> bool:
        for node_slot in self.map.values():
            if len(node_slot.collected) >= 2:
                return False

    def get_overfitted_values(self) -> list[tuple[Subject, Slot, Room, Instructor]]:
        return [
            items.collected for items in self.map.values() if len(items.collected) >= 2
        ]

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
        "__map"
    )
    def __init__(self, rooms: list[Room]):
        self.__map: dict[str, Day] = {
            room.room_id: Day() for room in rooms
        }

    def assign_event(
            self,
            *,
            subject: Subject,
            slot: Slot,
            room: Room,
            instructor: Optional[Instructor] = None,
    ) -> bool:
        target_slot = self.__map[room.room_id][slot.week_day][slot.start_time]
        if not target_slot.is_empty():
            return False
        target_slot.set_values(subject=subject, room=room, slot=slot, instructor=instructor)
        return True

    @property
    def map(self):
        return self.__map

    def get_room_schedule(self, room: Room) -> Day:
        return self.__map[room.room_id]

    def get_rooms_schedule(self) -> list[Day]:
        days = list(self.__map.values())
        return days

    def get_slots_in_room(self, room: Room, slot: Slot) -> Slots:
        return self.__map[room.room_id][slot.week_day]

    def __iter__(self) -> Generator[tuple[str, Day], None, None]:
        for room_id, day in self.__map.items():
            yield room_id, day
