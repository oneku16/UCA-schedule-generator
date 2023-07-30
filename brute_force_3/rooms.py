from datetime import datetime, timedelta
from typing import List, Tuple
from collections import defaultdict

from .subject import Subject
from config import DAYS


class Room:
    __slots__ = ('_room_id', '_capacity', '_room_name', 'days')

    def __init__(self, room_id, capacity, room_name):
        self._room_id = room_id
        self._capacity = capacity
        self._room_name = room_name
        self.days = [Days(day) for day in DAYS]

    @property
    def room_id(self):
        return self._room_id

    @property
    def capacity(self):
        return self._capacity

    @property
    def room_name(self):
        return self._room_name

    def __str__(self):
        return f'{self._room_name}'

    def __repr__(self):
        return (f'Room(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')

    def check_for_subject_week(self, subject: Subject):
        return not all(day.check_for_subject_day(subject=subject) for day in self.days)

    def is_slot_available(self) -> bool:
        return sum([day.is_slots() for day in self.days]) != len(self.days)

    def get_slots_for_subject(self, subject: Subject) -> defaultdict[list]:
        slots = defaultdict(list)
        for DAY, day in zip((0, 1, 2, 3), self.days):
            _status, _slots = day.slots_for_subject(subject=subject, _status=False)
            if _status:
                slots[DAY] = _slots
        return slots

    def get_schedule(self):
        schedule = dict()
        for day in self.days:
            schedule[day.day] = list()
            day: Days
            mapped = set()
            for index, value in enumerate(day.merged):
                if day.quarters[index + 1].subject is None:
                    continue
                if index in mapped:
                    continue
                if value is not None:
                    mapped.add(index)
                    schedule[day.day].append(
                        {
                                'end_time': day.quarters[index + 2].end_time,
                                'start_time': day.quarters[index + 1].start_time,
                                'subject': day.quarters[index + 1].subject,
                                'instructor': day.quarters[index + 1].subject.instructors.primary.instructor_name
                        }
                    )
                else:
                    # print(day.quarters[index + 1].subject.unique_id)
                    schedule[day.day].append(
                        {
                                'end_time': day.quarters[index + 1].end_time,
                                'start_time': day.quarters[index + 1].start_time,
                                'subject': str(day.quarters[index + 1].subject),
                                'instructor': day.quarters[index + 1].subject.instructors.primary.instructor_name
                        }
                    )
        return schedule


SLOTS = (
        {'start_time': '09:00', 'end_time': '10:30'},
        {'start_time': '11:00', 'end_time': '12:30'},
        {'start_time': '14:00', 'end_time': '15:30'},
        {'start_time': '16:00', 'end_time': '17:30'},
)


class Quarter:
    __slots__ = ('__default', 'start_time', 'end_time', 'status', 'subject')

    def __init__(self, start_time, end_time):
        self.__default = start_time, end_time
        self.start_time = start_time
        self.end_time = end_time
        self.subject = None
        self.status = False

    def reset(self):
        self.start_time, self.end_time = self.__default
        self.status = False
        self.subject = None


class Days:
    __slots__ = ('day', 'quarters', 'merged')

    def __init__(self, day):
        self.day = day
        self.quarters = {quarter: Quarter(**SLOT) for quarter, SLOT in enumerate(SLOTS, 1)}
        self.merged = [None] * len(self.quarters)

    def check_for_subject_day(self, subject: Subject) -> bool:
        for quarter in self.quarters.values():
            if quarter.subject and f'{quarter.subject.id_}{quarter.subject.cohort}' == f'{subject.id_}{subject.cohort}':
                return True
        return False

    def is_slots(self) -> bool:
        return sum([slot.status for slot in self.quarters.values()]) != len(self.quarters)

    @staticmethod
    def __is_fit_instructor_time(instructors, *quarters):
        if instructors.primary.preferences.time_preferences is False:
            return True
        slot_start_time, slots_end_time = quarters[0].start_time, quarters[-1].end_time
        __format, __date = '%Y-%m-%d %H:%M', "1900-01-01 "
        instructor_start_time = datetime.strptime(__date + instructors.primary.preferences.start_time, __format).time()
        instructor_end_time = datetime.strptime(__date + instructors.primary.preferences.end_time, __format).time()
        return instructor_start_time <= slot_start_time and instructor_end_time >= slots_end_time

    def slots_for_subject(self, subject: Subject, _status=True) -> bool | Tuple[bool, List[Tuple]]:
        slots = list()
        if subject.duration <= 120:
            _slots = (1, 2, 3, 4)
            for quarter in _slots:
                status_quarter = self.quarters[quarter].status is False
                status_instructor_preferences = self.__is_fit_instructor_time(subject.instructors, self.quarters[quarter])
                if status_quarter is status_instructor_preferences is True:
                    slots.append(quarter)
        else:
            _slots = ((1, 2), (3, 4))
            for first_quarter, second_quarter in _slots:
                status_quarter = self.quarters[first_quarter].status is self.quarters[second_quarter].status is False
                status_instructor_preferences = self.__is_fit_instructor_time(subject.instructors, self.quarters[first_quarter], self.quarters[second_quarter])
                if status_quarter is status_instructor_preferences is True:
                    slots.append((first_quarter, second_quarter))
        if _status:
            return slots != []
        return len(slots) >= 1, slots

    def is_merged(self, slot_index: int, status_only: bool = True) -> tuple[bool | int, int] | bool:
        slots = ((0, 1), (2, 3))
        for first, second in slots:
            if slot_index == first and self.merged[first] == self.merged[second] and self.merged[first] is not None and self.merged[second] is not None:
                return True if status_only else first, second
        return False

    def __merge(self, first_slot, second_slot) -> None:
        self.merged[first_slot - 1] = min(first_slot, second_slot)
        self.merged[second_slot - 1] = min(first_slot, second_slot)

    def __undo_merge(self, first_slot, second_slot) -> None:
        self.merged[first_slot - 1] = None
        self.merged[second_slot - 1] = None

    @staticmethod
    def __get_true_time(quarter_start_time, quarter_end_time, subject_duration) -> str:
        start_time = datetime.strptime(quarter_start_time, '%H:%M')
        end_time = datetime.strptime(quarter_end_time, '%H:%M')
        true_time = min(start_time + timedelta(minutes=subject_duration), end_time)
        return true_time.strftime('%H:%M')

    def set_subject(self, slot: tuple[int, int] | int, subject: Subject) -> None:
        if isinstance(slot, tuple):
            first_slot, second_slot = slot
            self.__merge(first_slot=first_slot, second_slot=second_slot)
            self.quarters[first_slot].status = True
            self.quarters[second_slot].status = True
            self.quarters[first_slot].subject = subject
            self.quarters[second_slot].end_time = self.__get_true_time(
                quarter_start_time=self.quarters[first_slot].start_time,
                quarter_end_time=self.quarters[second_slot].end_time,
                subject_duration=subject.duration
            )

        else:
            self.quarters[slot].status = True
            self.quarters[slot].subject = subject
            self.quarters[slot].end_time = self.__get_true_time(
                quarter_start_time=self.quarters[slot].start_time,
                quarter_end_time=self.quarters[slot].end_time,
                subject_duration=subject.duration
            )

    def remove_subject(self, subject: Subject):
        for quarter, slot in self.quarters.items():
            slot: Quarter
            if subject is slot.subject:
                if subject.duration > 120:
                    self.__undo_merge(quarter, quarter + 1)
                    self.quarters[quarter].reset()
                    self.quarters[quarter + 1].reset()
                    return
                else:
                    self.quarters[quarter].reset()
                    return
        # raise 'wrong subject'

    def get_slot(self, subject: Subject) -> bool | tuple | int:
        if subject.duration <= 120:
            for quarter, slot in self.quarters.items():
                slot: Quarter
                if subject.instructors.primary.preferences.time_preferences:
                    start, end = subject.instructors.preferences.start_time, subject.instructors.preferences.end_time
                    if not slot.status and start <= slot.start_time and slot.end_time <= end:
                        return quarter
                else:
                    if not slot.status:
                        return quarter
        else:
            double_quarters = ((1, 2), (3, 4))
            for first, second in double_quarters:
                first_slot: Quarter = self.quarters.get(first)
                second_slot: Quarter = self.quarters.get(second)
                if subject.instructors['primary']['preferences']:
                    start, end = subject.instructors['primary']['start_hour'], subject.instructors['primary'][
                        'end_hour']
                    if not first_slot.status and not second_slot.status and start <= first_slot.start_time and second_slot.end_time <= end:
                        return first, second
                else:
                    if not first_slot.status and not second_slot.status:
                        return first, second

        return False

    def __str__(self):
        return self.day

    def __repr__(self):
        return f'Quarters(day={self.day})'


class LectureRoom(Room):

    def __init__(self, room_id, capacity, room_name):
        super().__init__(room_id, capacity, room_name)

    def __repr__(self):
        return (f'LectureRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')


class TutorialRoom(Room):

    def __init__(self, room_id, capacity, room_name):
        super().__init__(room_id, capacity, room_name)

    def __repr__(self):
        return (f'TutorialRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')


class LaboratoryRoom(Room):

    def __init__(self, room_id, capacity, room_name):
        super().__init__(room_id, capacity, room_name)

    def __repr__(self):
        return (f'LaboratoryRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')


class PhysicalTrainingRoom(Room):

    def __init__(self, room_id, capacity, room_name):
        super().__init__(room_id, capacity, room_name)

    def __repr__(self):
        return (f'BabbleRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')


def get_room(room_id, capacity, room_type, room_name):
    if room_type == 'lecture':
        return LectureRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'tutorial':
        return TutorialRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'laboratory':
        return LaboratoryRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'physical_training':
        return PhysicalTrainingRoom(room_id=room_id, capacity=capacity, room_name=room_name)
