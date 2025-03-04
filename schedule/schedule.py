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

    def set_values(
            self,
            subject: Subject,
            room: Room,
            slot: Slot,
            instructor: Instructor,
    ) -> None:
        self.subject = subject
        self.room = room
        self.slot = slot
        self.instructor = instructor

    def __repr__(self) -> str:
        return f'NodeSlot(subject={self.subject}, room={self.room}, slot={self.slot}, instructor={self.instructor})'


class NodeDay(Node):
    __slots__ = Node.__slots__ + (
        "slot",
    )
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.slot: Optional['Slots'] = None

    def set_values(self, slot: 'Slots') -> None:
        self.slot = slot


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
        if self.pointer == self.head or self.pointer is None:
            return None
        self.pointer = self.pointer.prev_node
        return self.pointer

    def forward(self) -> Node | None:
        if self.pointer == self.tail or self.pointer is None:
            return None
        self.pointer = self.pointer.next_node
        return self.pointer


class Slots(LinkedListMapBase):
    def __init__(self) -> None:
        super().__init__()

        for name in SLOTS:
            node = NodeSlot(name)
            self.map[name] = node
            node.prev_node = self.tail.prev_node
            node.next_node = self.tail
            self.tail.prev_node.next_node = node
            self.tail.prev_node = node

        self.pointer = self.head.next_node

    def __iter__(self) -> Generator[tuple[Subject, Slot, Room, Instructor], None, None]:

        dummy: NodeSlot = self.head.next_node
        while dummy != self.tail:
            yield dummy.subject, dummy.slot, dummy.room, dummy.instructor,

            dummy = dummy.next_node


class Days(LinkedListMapBase):
    def __init__(self) -> None:
        super().__init__()

        for name in DAYS:
            node = NodeDay(name)
            node.slot = Slots()
            self.map[name] = node
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


class RoomSchedule:
    __slots__ = (
        "__map",
    )
    def __init__(self):
        self.__map = {
        }


class Schedule:
    __slots__ = (
        "schedule",
        "rooms"
    )
    def __init__(self, rooms: list[Room]):
        self.rooms = {
            room.room_id: list() for room in rooms
        }
