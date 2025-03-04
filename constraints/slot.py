from datetime import time, timedelta, datetime
from time import strptime
from random import choice

from config import DAYS, SLOTS


class Slot:
    __slots__ = (
        "__week_day",
        "__start_time",
        "__end_time",
        "__duration",
    )
    slot_start: tuple[str] = tuple(
        f"{slot['hour']}:{slot['minute']}" for slot in SLOTS
    )

    def __init__(self, duration: int, week_day: str = None, start_time: str = None) -> None:
        self.__week_day = week_day
        self.__start_time = start_time
        self.__end_time = None
        self.__duration = duration

    def __repr__(self) -> str:
        return f'Slot(weekday={self.__week_day}, start_time={self.__start_time}, end_time={self.__end_time})'

    @property
    def week_day(self) -> str:
        return self.__week_day

    @week_day.setter
    def week_day(self, value: str) -> None:
        self.__week_day = value

    @property
    def start_time(self) -> str:
        return self.__start_time

    @start_time.setter
    def start_time(self, value: str) -> None:
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
        parsed_time = datetime.strptime(self.__start_time, "%H:%M")
        new_time = parsed_time + timedelta(minutes=self.__duration)
        self.__end_time = new_time.strftime("%H:%M")

    def update_values(self, start_time: str = None, week_day: str = None) -> None:
        if start_time is None:
            self.__start_time = choice(self.slot_start)
        else:
            self.__start_time = start_time

        if week_day is None:
            self.__week_day = choice(DAYS)
        else:
            self.__week_day = week_day
        self.__update_end_time()
