from types import MappingProxyType
from typing import Optional, Any


class Room:
    """
    Represents a room with its ID, capacity, type, and additional constraints.

    Attributes:
        room_id (str): A unique identifier for the room.
        capacity (int): The maximum number of people the room can accommodate.
        room_type (str): The type of the room (e.g., "lecture", "lab").
        extra_constraints (MappingProxyType): Additional constraints for the room. Read-only.
    """
    __slots__ = (
        "room_id",
        "capacity",
        "room_type",
        "extra_constraints",
    )

    def __init__(
            self,
            room_id: str,
            capacity: int,
            room_type: str,
            **extra_constraints: Optional[dict[str, Any]],
    ):
        """
        Initializes a Room instance.
        Args:
            room_id (str): A unique identifier for the room.
            capacity (int): The maximum number of people the room can accommodate.
            room_type (str): The type of the room (e.g., "lecture", "lab").
            extra_constraints (Optional[dict[str, Any]]): Additional constraints for the room. Defaults to None.
        Raises:
            ValueError: If `room_id` or `room_type` is empty, or if `capacity` is not a positive integer.
        """
        if not isinstance(room_id, str) or not room_id:
            raise ValueError("room_id must be a non-empty string")
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        if not isinstance(room_type, str) or not room_type:
            raise ValueError("room_type must be a non-empty string")

        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.extra_constraints = extra_constraints or {}

    def __repr__(self):
        return f'Room(id={self.room_id}, type={self.room_type})'

    def __eq__(self, other: 'Room'):
        """
        Checks if two Room instances are equal based on their `room_id`.
        Args:
            other (Any): The object to compare with.
        Returns:
            bool: True if the objects are equal, otherwise False.
        """
        return self.room_id == other.room_id

    def __hash__(self):
        """
        Returns a hash value for the Room instance based on its `room_id`.
        Returns:
            int: The hash value.
        """
        return hash(self.room_id)
