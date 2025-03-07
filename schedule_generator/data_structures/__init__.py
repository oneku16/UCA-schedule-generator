"""
data_structures package

This package provides data structures for managing schedules, rooms, and linked lists.

Modules:
    - dictionaries: Contains the ScheduleDictionary class for managing schedules.
    - room_selector: Contains the RoomSelector class for managing room availability.
    - linked_list_ds: Contains classes for managing linked lists (Day, Slots, NodeDay, NodeSlot).

Classes:
    - ScheduleDictionary: A dictionary-like class for managing schedules.
    - RoomSelector: A class for managing room availability and selection.
    - Days: A class representing a collection of days in a schedule.
    - Slots: A class representing a collection of time slots in a weekday.
    - NodeDay: A class representing a node for a day in a linked list.
    - NodeSlot: A class representing a node for a time slot in a linked list.
"""

from .dictionaries import ScheduleDictionary
from .room_selector import RoomSelector
from .linked_list_ds import Days, Slots, NodeDay, NodeSlot


# Define __all__ for explicit exports
__all__ = [
    "ScheduleDictionary",
    "RoomSelector",
    "Days",
    "Slots",
    "NodeDay",
    "NodeSlot",
]
