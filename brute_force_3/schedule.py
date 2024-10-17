from config import DAYS
from brute_force_3.rooms import Days


class Schedule:
    def __init__(self, cohort_name: str):
        self.cohort_name = cohort_name
        self.days = [Days(day) for day in DAYS]
        self.days_mapped = {a: b for a, b in zip(DAYS, self.days)}

    def __getitem__(self, item) -> Days:
        return self.days_mapped[item]
