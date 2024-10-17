from typing import Iterator

from config import DAYS
from .slot import Slot


class Schedule:
    def __init__(self, cohorts_list):
        self.cohorts_list: list[str] = cohorts_list
        self.cohorts: dict[str, dict[str, Slot]] = {
                cohort_name: {
                        day: Slot() for day in DAYS
                } for cohort_name in self.cohorts_list
        }

    def __iter__(self) -> Iterator[tuple[str, dict[str, Slot]]]:
        for cohort_name, days in self.cohorts.items():
            yield cohort_name, days

    def __repr__(self):
        return str(self.cohorts)
