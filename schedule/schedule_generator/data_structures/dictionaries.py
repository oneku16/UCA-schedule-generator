from collections import defaultdict
from typing import Generator

from schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor

# Define a type alias for readability
SubjectList = list[tuple[Subject, Slot, Room, Instructor]]


class ScheduleDictionary:
    """
    A dictionary-like class for storing and managing schedules, where each key is a Subject instance
    and each value is a list of schedules (each schedule is a list of [Subject, Slot, Room, Instructor]).
    """
    __slots__ = ("__map",)

    def __init__(self):
        """
        Initializes a ScheduleDictionary instance.
        """
        self.__map: defaultdict[Subject, list[SubjectList]] = defaultdict(list)

    def __setitem__(self, subject: Subject, schedule: SubjectList):
        """
        Adds a schedule for the given Subject instance.
        Args:
            subject (Subject): The Subject instance.
            schedule (SubjectList): A list containing [Subject, Slot, Room, Instructor].
        Raises:
            ValueError: If `schedule` is not a list of [Subject, Slot, Room, Instructor].
        """
        if not isinstance(schedule, list) or len(schedule) != 4:
            raise ValueError("schedule must be a list of [Subject, Slot, Room, Instructor]")
        self.__map[subject].append(schedule)

    def __getitem__(self, subject: Subject) -> list[SubjectList]:
        """
        Returns the list of schedules for the given Subject instance.
        Args:
            subject (Subject): The Subject instance.
        Returns:
            list[SubjectList]: The list of schedules for the subject.
        """
        return self.__map[subject]

    def __contains__(self, subject: Subject) -> bool:
        """
        Checks if the given Subject instance exists in the dictionary.
        Args:
            subject (Subject): The Subject instance.
        Returns:
            bool: True if the subject exists, otherwise False.
        """
        return subject in self.__map

    def __repr__(self) -> str:
        """
        Returns a string representation of the ScheduleDictionary.
        Returns:
            str: The string representation.
        """
        return repr(self.__map)

    def __iter__(self) -> Generator[tuple[Subject, list[SubjectList]], None, None]:
        """
        Iterates over the dictionary, yielding Subject instances and their associated schedules.
        Yields:
            tuple[Subject, list[SubjectList]]: A tuple containing the Subject instance and its schedules.
        """
        for subject, schedules in self.__map.items():
            yield subject, schedules
