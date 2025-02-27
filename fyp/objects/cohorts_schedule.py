from typing import Iterator

from config import DAYS
from .slot import Slot
from .schedule import Schedule


class CohortsSchedule:
    def __init__(self, cohorts_list):
        self.cohorts_list: list[str] = cohorts_list
        self.cohorts: dict[str, Schedule] = {
                cohort_name: Schedule() for cohort_name in self.cohorts_list
        }

    def __iter__(self) -> Iterator[tuple[str, Schedule]]:
        for cohort_name, schedule in self.cohorts.items():
            yield cohort_name, schedule

    def __repr__(self):
        return str(self.cohorts)
