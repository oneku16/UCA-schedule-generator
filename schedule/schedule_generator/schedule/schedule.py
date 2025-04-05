from collections import defaultdict
from typing import Optional, Generator

from schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor
from schedule.schedule_generator.data_structures import Days, Slots


class Schedule:
    """
    A class for managing and assigning events (subjects, slots, rooms, and instructors) in a schedule.

    The class maintains two main data structures:
    - `__room_map`: A dictionary mapping room IDs to `Days` objects, representing the schedule for each room.
    - `__subject_map`: A dictionary mapping subject IDs to lists of `Slot` objects, representing the slots assigned to each subject.
    Attributes:
        __room_map (dict[str, Days]): A dictionary mapping room IDs to their respective schedules.
        __subject_map (defaultdict[str, list[Slot]]): A dictionary mapping subject IDs to lists of assigned slots.
    """
    __slots__ = ("__room_map", "__subject_map")

    def __init__(self, rooms: list[Room]):
        """
        Initializes a Schedule instance.
        Args:
            rooms (list[Room]): A list of Room instances to include in the schedule.
        """
        self.__room_map: dict[str, Days] = {
            room.room_id: Days() for room in rooms
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
        """
        Assigns an event (subject, slot, room, and optionally an instructor) to the schedule.
        Args:
            subject (Subject): The subject to assign.
            slot (Slot): The time slot to assign.
            room (Room): The room to assign.
            instructor (Optional[Instructor]): The instructor to assign. Defaults to None.
        Returns:
            bool: True if the event was successfully assigned, False if the slot is already occupied.
        """
        target_slot = self.__room_map[room.room_id][slot.week_day][slot.start_time]
        if not target_slot.is_empty():
            return False
        target_slot.set_values(subject=subject, room=room, slot=slot, instructor=instructor)
        self.__subject_map[subject.subject_full_id].append(slot)
        return True

    @property
    def room_map(self) -> dict[str, Days]:
        """
        Returns the internal room map.
        Returns:
            dict[str, Days]: A dictionary mapping room IDs to their respective schedules.
        """
        return self.__room_map

    @property
    def subject_map(self) -> defaultdict[str, list[Slot]]:
        """
        Returns the internal subject map.
        Returns:
            defaultdict[str, list[Slot]]: A dictionary mapping subject IDs to lists of assigned slots.
        """
        return self.__subject_map

    def get_room_schedule(self, room: Room) -> Days:
        """
        Returns the schedule for a specific room.
        Args:
            room (Room): The room to retrieve the schedule for.
        Returns:
            Days: The schedule for the specified room.
        """
        return self.__room_map[room.room_id]

    def get_rooms_schedule(self) -> list[Days]:
        """
        Returns the schedules for all rooms.
        Returns:
            list[Days]: A list of schedules for all rooms.
        """
        days = list(self.__room_map.values())
        return days

    def get_slots_in_room(self, room: Room, slot: Slot) -> Slots:
        """
        Returns the slots for a specific room and day.
        Args:
            room (Room): The room to retrieve the slots for.
            slot (Slot): The slot containing the day to retrieve.
        Returns:
            Slots: The slots for the specified room and day.
        """
        return self.__room_map[room.room_id][slot.week_day]

    def __iter__(self) -> Generator[tuple[str, Days], None, None]:
        """
        Iterates over the room map, yielding room IDs and their respective schedules.
        Yields:
            tuple[str, Days]: A tuple containing the room ID and its schedule.
        """
        for room_id, day in self.__room_map.items():
            yield room_id, day
