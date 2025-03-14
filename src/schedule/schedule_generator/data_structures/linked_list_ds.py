from typing import Generator, TypeVar, Optional

from src.schedule.consts import DAYS, SLOTS
from .dictionaries import ScheduleDictionary
from src.schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor


# Precompute slots as a tuple of strings in "HH:MM" format
slots: tuple[str, ...] = tuple(f"{slot['hour']}:{slot['minute']}" for slot in SLOTS)


# Define a TypeVar for Node types
NodeType = TypeVar('NodeType', bound='Node')


class Node:
    """
    A base class representing a node in a linked list.
    Attributes:
        name (Optional[str]): The name of the node.
        prev_node (Optional[NodeType]): The previous node in the linked list.
        next_node (Optional[NodeType]): The next node in the linked list.
    """
    __slots__ = ("name", "prev_node", "next_node")

    def __init__(
        self,
        name: Optional[str] = None,
        prev_node: Optional[NodeType] = None,
        next_node: Optional[NodeType] = None,
    ) -> None:
        """
        Initializes a Node instance.
        Args:
            name (Optional[str]): The name of the node. Defaults to None.
            prev_node (Optional[NodeType]): The previous node in the linked list. Defaults to None.
            next_node (Optional[NodeType]): The next node in the linked list. Defaults to None.
        """
        self.name = name
        self.prev_node = prev_node
        self.next_node = next_node

    def set_values(self, *args, **kwargs) -> None:
        """
        Sets values for the node. This method should be overridden by subclasses.
        Raises:
            NotImplementedError: If the method is not overridden.
        """
        raise NotImplementedError()


class NodeSlot(Node):
    """
    A class representing a node for a time slot in a schedule.
    Attributes:
        subject (Optional[Subject]): The subject associated with the slot.
        room (Optional[Room]): The room associated with the slot.
        slot (Optional[Slot]): The time slot.
        instructor (Optional[Instructor]): The instructor associated with the slot.
    """
    __slots__ = Node.__slots__ + ("subject", "room", "slot", "instructor", "collected")

    def __init__(
        self,
        name: Optional[str] = None,
        subject: Optional[Subject] = None,
        room: Optional[Room] = None,
        slot: Optional[Slot] = None,
        instructor: Optional[Instructor] = None,
    ) -> None:
        """
        Initializes a NodeSlot instance.
        Args:
            name (Optional[str]): The name of the node. Defaults to None.
            subject (Optional[Subject]): The subject associated with the slot. Defaults to None.
            room (Optional[Room]): The room associated with the slot. Defaults to None.
            slot (Optional[Slot]): The time slot. Defaults to None.
            instructor (Optional[Instructor]): The instructor associated with the slot. Defaults to None.
        """
        super().__init__(name=name)
        self.subject = subject
        self.room = room
        self.slot = slot
        self.instructor = instructor

    def is_empty(self) -> bool:
        """
        Checks if the node is empty (i.e., has no subject assigned).
        Returns:
            bool: True if the node is empty, otherwise False.
        """
        return self.subject is None

    def get_data(self) -> tuple[Subject, Slot, Room, Instructor]:
        """
        Returns the data associated with the node.
        Returns:
            tuple[Subject, Slot, Room, Instructor]: The subject, slot, room, and instructor.
        """
        return self.subject, self.slot, self.room, self.instructor

    def set_values(
        self,
        *,
        subject: Optional[Subject] = None,
        slot: Optional[Slot] = None,
        room: Optional[Room] = None,
        instructor: Optional[Instructor] = None,
    ) -> None:
        """
        Sets values for the node if it is empty.
        Args:
            subject (Optional[Subject]): The subject to assign. Defaults to None.
            slot (Optional[Slot]): The time slot to assign. Defaults to None.
            room (Optional[Room]): The room to assign. Defaults to None.
            instructor (Optional[Instructor]): The instructor to assign. Defaults to None.
        """
        if self.is_empty():
            self.subject = subject
            self.room = room
            self.slot = slot
            self.instructor = instructor

    def __repr__(self) -> str:
        """
        Returns a string representation of the NodeSlot.
        Returns:
            str: The string representation.
        """
        return f"NodeSlot(name={self.name}, subject={self.subject}, room={self.room}, slot={self.slot}, instructor={self.instructor})"


class NodeDay(Node):
    """
    A class representing a node for a day in a schedule.
    Attributes:
        slot (Optional[Slots]): The slots associated with the day.
    """
    __slots__ = Node.__slots__ + ("slot",)

    def __init__(self, name: str, slot: Optional['Slots'] = None) -> None:
        """
        Initializes a NodeDay instance.
        Args:
            name (str): The name of the day.
            slot (Optional[Slots]): The slots associated with the day. Defaults to None.
        """
        super().__init__(name)
        self.slot = slot

    def set_values(self, slot: 'Slots') -> None:
        """
        Sets the slots for the day.
        Args:
            slot (Slots): The slots to assign.
        """
        self.slot = slot

    def __repr__(self) -> str:
        """
        Returns a string representation of the NodeDay.
        Returns:
            str: The string representation.
        """
        return f"NodeDay(day={self.name}, slot={self.slot})"

    def __getitem__(self, start_time: str) -> 'NodeSlot':
        """
        Returns the slot associated with the given start time.
        Args:
            start_time (str): The start time of the slot.
        Returns:
            NodeSlot: The slot associated with the start time.
        """
        return self.slot[start_time]


class LinkedListMapBase:
    """
    A base class for managing a doubly linked list with a dictionary for fast lookups.
    Attributes:
        head (Node): The head sentinel node of the linked list.
        tail (Node): The tail sentinel node of the linked list.
        pointer (Optional[Node]): A pointer to the current node in the linked list.
        map (dict): A dictionary for fast lookups of nodes.
    """
    __slots__ = ("head", "tail", "pointer", "map")

    def __init__(self):
        """
        Initializes a LinkedListMapBase instance.
        """
        self.head: Node = Node(None)
        self.tail: Node = Node(None)
        self.head.next_node = self.tail
        self.tail.prev_node = self.head
        self.map = dict()
        self.pointer: Optional[Node] = None

    def backward(self) -> Optional[Node]:
        """
        Moves the pointer to the previous node in the linked list.
        Returns:
            Optional[Node]: The previous node, or None if the pointer is at the head.
        """
        if self.pointer is self.head.next_node:
            return None
        self.pointer = self.pointer.prev_node
        return self.pointer

    def forward(self) -> Optional[Node]:
        """
        Moves the pointer to the next node in the linked list.
        Returns:
            Optional[Node]: The next node, or None if the pointer is at the tail.
        """
        if self.pointer is self.tail.prev_node:
            return None
        self.pointer = self.pointer.next_node
        return self.pointer

    def pointer_iter(self) -> Generator[Node, None, None]:
        """
        Iterates over the linked list using the pointer.
        Yields:
            Node: The current node in the iteration.
        """
        self.pointer = self.head.next_node
        while self.pointer != self.tail:
            yield self.pointer
            self.pointer = self.pointer.next_node
        self.pointer = self.head.next_node


class Slots(LinkedListMapBase):
    """
    A class representing a collection of time slots in a schedule.
    Attributes:
        pointer (NodeSlot): A pointer to the current slot in the linked list.
    """
    def __init__(self) -> None:
        """
        Initializes a Slots instance.
        """
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
        """
        Checks if all slots are occupied.
        Returns:
            bool: True if all slots are occupied, otherwise False.
        """
        for node_slot in self.map.values():
            if node_slot.is_empty():
                return False
        return True

    def get_schedule(self) -> ScheduleDictionary:
        """
        Returns a dictionary representation of the schedule.
        Returns:
            ScheduleDictionary: The schedule as a dictionary.
        """
        schedule_dictionary = ScheduleDictionary()
        curr = self.head.next_node
        while curr != self.tail:
            if not curr.is_empty():
                schedule_dictionary[curr.subject].append(curr.get_data())
            curr = curr.next_node
        return schedule_dictionary

    def __iter__(self) -> Generator[tuple[Subject, Slot, Room, Instructor], None, None]:
        """
        Iterates over the slots and yields their data.
        Yields:
            tuple[Subject, Slot, Room, Instructor]: The data associated with each slot.
        """
        dummy: NodeSlot = self.head.next_node
        while dummy != self.tail:
            yield dummy.subject, dummy.slot, dummy.room, dummy.instructor
            dummy = dummy.next_node

    def __getitem__(self, start_time: str) -> NodeSlot:
        """
        Returns the slot associated with the given start time.
        Args:
            start_time (str): The start time of the slot.
        Returns:
            NodeSlot: The slot associated with the start time.
        """
        return self.map[start_time]

    def __repr__(self) -> str:
        """
        Returns a string representation of the Slots.
        Returns:
            str: The string representation.
        """
        return f"Slots({', '.join(map(str, self.map.items()))})"


class Days(LinkedListMapBase):
    """
    A class representing a collection of days in a schedule.
    Attributes:
        pointer (NodeDay): A pointer to the current day in the linked list.
    """
    def __init__(self) -> None:
        """
        Initializes a Day instance.
        """
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
        """
        Returns a dictionary representation of the schedule.
        Returns:
            ScheduleDictionary: The schedule as a dictionary.
        """
        schedule_dictionary = ScheduleDictionary()
        curr_day = self.head.next_node
        while curr_day != self.tail:
            if not curr_day.is_empty():
                curr_slot = curr_day.head.next_node
                while curr_slot != curr_day.tail:
                    if not curr_slot.is_empty():
                        schedule_dictionary[curr_slot.subject].append(curr_slot.get_data())
                    curr_slot = curr_slot.next_node
            curr_day = curr_day.next_node
        return schedule_dictionary

    def __iter__(self) -> Generator[Slots, None, None]:
        """
        Iterates over the days and yields their slots.
        Yields:
            Slots: The slots associated with each day.
        """
        dummy: NodeDay = self.head.next_node
        while dummy != self.tail:
            yield dummy.slot
            dummy = dummy.next_node

    def __getitem__(self, week_day: str) -> Slots:
        """
        Returns the slots associated with the given day.
        Args:
            week_day (str): The name of the day.
        Returns:
            Slots: The slots associated with the day.
        """
        return self.map[week_day]
