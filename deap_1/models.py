from dataclasses import dataclass


@dataclass(kw_only=True, slots=True, frozen=True)
class Room:
    room_id: int | str
    room_name: str
    room_capacity: int
    room_type: str


@dataclass(kw_only=True, slots=True, frozen=True)
class Cohort:
    cohort_id: int | str
    cohort_name: str
    cohort_year: int
    number_of_students: int


@dataclass(kw_only=True, slots=True, frozen=True)
class Subject:
    subject_id: int | str
    subject_name: str
    teacher_id: int | str
    number_of_hours = number_of_hours
