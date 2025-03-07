from datetime import time, timedelta, datetime
from random import choice
from typing import Optional

from consts import DAYS, SLOTS


class Slot:
    """
    Represents a time slot with a specific duration, weekday, and start/end times.
    Attributes:
        __week_day (str): The day of the week for the slot.
        __start_time (str): The start time of the slot in 'HH:MM' format.
        __end_time (str): The end time of the slot in 'HH:MM' format.
        __duration (int): The duration of the slot in minutes.
    """
    __slots__ = (
        "__week_day",
        "__start_time",
        "__end_time",
        "__duration",
    )
    slot_start: tuple[str, ...] = tuple(
        f"{slot['hour']}:{slot['minute']}" for slot in SLOTS
    )

    def __init__(
            self,
            duration: int,
            week_day: Optional[str] = None,
            start_time: Optional[str] = None,
    ) -> None:
        """
        Initializes a Slot instance.
        Args:
            duration (int): The duration of the slot in minutes.
            week_day (Optional[str]): The day of the week for the slot. Defaults to None.
            start_time (Optional[str]): The start time of the slot in 'HH:MM' format. Defaults to None.
        Raises:
            ValueError: If `duration` is not a positive integer, `week_day` is not in `DAYS`,
                       or `start_time` is not in 'HH:MM' format.
        """
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("duration must be a positive integer")
        if week_day is not None and week_day not in DAYS:
            raise ValueError(f"week_day must be one of {DAYS}")
        if start_time is not None and not isinstance(start_time, str):
            raise ValueError("start_time must be a string in 'HH:MM' format")

        self.__duration = duration
        self.__week_day = week_day
        self.__start_time = start_time
        self.__end_time = None
        if self.__start_time is not None:
            self.__update_end_time()

    @property
    def week_day(self) -> str:
        return self.__week_day

    @week_day.setter
    def week_day(self, value: str) -> None:
        if value not in DAYS:
            raise ValueError(f"week_day must be one of {DAYS}")
        self.__week_day = value

    @property
    def start_time(self) -> str:
        return self.__start_time

    @start_time.setter
    def start_time(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("start_time must be a string in 'HH:MM' format")
        self.__start_time = value
        self.__update_end_time()

    @property
    def end_time(self) -> str:
        if self.__end_time is None:
            self.__update_end_time()
        return self.__end_time

    @property
    def start_time_iso_format(self) -> time:
        return time.fromisoformat(self.__start_time)

    @property
    def end_time_iso_format(self) -> time:
        return time.fromisoformat(self.__end_time)

    def __update_end_time(self) -> None:
        """
        Updates the end time based on the start time and duration.
        """
        try:
            parsed_time = datetime.strptime(self.__start_time, "%H:%M")
        except ValueError as e:
            raise ValueError(f"Invalid start_time format: {e}")
        new_time = parsed_time + timedelta(minutes=self.__duration)
        self.__end_time = new_time.strftime("%H:%M")

    def update_values(self, start_time: Optional[str] = None, week_day: Optional[str] = None) -> None:
        """
        Updates the start time and/or week day of the slot.
        Args:
            start_time (Optional[str]): The new start time in 'HH:MM' format. Defaults to a random value.
            week_day (Optional[str]): The new day of the week. Defaults to a random value.
        """
        self.__start_time = start_time or choice(self.slot_start)
        self.__week_day = week_day or choice(DAYS)

        self.__update_end_time()

    def __eq__(self, other):
        """
        Checks if two Slot instances are equal based on their `week_day` and `start_time`.
        Args:
            other (Any): The object to compare with.
        Returns:
            bool: True if the objects are equal, otherwise False.
        """
        if not isinstance(other, Slot):
            raise TypeError("other must be an instance of Slot.")
        return self.__week_day == other.__week_day and self.__start_time == other.__start_time

    def __hash__(self):
        """
        Returns a hash value for the Slot instance based on its `week_day` and `start_time`.
        Returns:
            int: The hash value.
        """
        return hash((self.__week_day, self.__start_time))

    def __repr__(self) -> str:
        return f'Slot(weekday={self.__week_day}, start_time={self.__start_time}, end_time={self.__end_time})'
