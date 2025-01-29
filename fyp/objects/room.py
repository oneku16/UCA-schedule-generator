from collections.abc import Iterable

from .subject import Subject
from .slot import Slot
from config import DAYS


class Room:
    def __init__(
            self,
            room_id: str,
            capacity: int,
            room_type: str,
            **extra_constraints
    ):
        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.extra_constraints = extra_constraints
        self.room_schedule: dict[str, Slot] = {day: Slot() for day in DAYS}

    def add_subject(self, day: str, index: int, subject: Subject):
        assert day in DAYS
        assert 0 <= index <= 3
        self.room_schedule[day].add_subject(
            quarter=index,
            mapped_objects={
                'subject': subject,
                'room': self}
        )

    def subject_match(self, subject: Subject) -> tuple[bool, bool, bool]:
        """
        Checks if the given subject's requirements and optional_requirements
        matches the class constraints.
        :param subject: Subject type
        :return: [bool, bool]
        """
        requirements = subject.requirements
        optional_requirements = subject.optional_requirements

        is_room_match = is_requirements_match = is_optional_requirements_match = True

        is_room_match &= self.room_type in subject.preferred_rooms

        if requirements is None and optional_requirements is None:
            return is_room_match, is_requirements_match, is_optional_requirements_match

        for key, value in requirements.items():
            is_requirements_match &= self.extra_constraints.get(key) == value

        for key, value in optional_requirements.items():
            is_optional_requirements_match &= self.extra_constraints.get(key) == value

        return is_room_match, is_requirements_match, is_optional_requirements_match

    def is_empty_slot(self) -> bool:
        """
        checks if the room has empty slots.
        :return: True if room has empty slots, False otherwise
        """
        return any(not slot.is_full() for _, slot in self.room_schedule.items())

    def get_empty_slots(self, subject: Subject) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
        """
        finds a slots from the room, first it tries to get slot
        such that it is in the same row with other same subjects, but in different column.
        If no slot is found from the same row, it finds slot from new row and returns it.
        Make sure that room has empty slots.
        :return: dict[str, int] -> day name and slot index.
        """

        day_map: dict[str, list[int]] = dict()

        for day, slot in self.room_schedule.items():
            if not slot.is_full():
                quarters: list[int] = list(slot.get_empty_quarters())
                day_map[day] = quarters

        day_map_c: dict[str, list[int]] = dict()
        for day, quarters in day_map.items():
            if any(
                    value['subject'].subject_full_id == subject.subject_full_id
                    for value in self.room_schedule[day].subjects_list
            ):
                continue
            day_map_c[day] = quarters

        return day_map_c, day_map

    def transfer_subjects(self, room: "Room", *subjects: Iterable[Subject]) -> None:
        ...

    def __repr__(self):
        return f'Room(id={self.room_id}, type={self.room_type}, schedule={self.room_schedule})'
