from datetime import datetime, timedelta
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

    def get_schedule(self):
        schedule = dict()
        for day in self.days:
            schedule[day] = list()
            day: Days
            mapped = set()

            for index, value in day.merged:
                if index in mapped:
                    continue
                if value is not None:
                    mapped.add(index)
                    schedule[day].append(
                        {
                                'start_time': day.quarters[index + 1].start_time,
                                'end_time': day.quarters[index + 2].end_time,
                                'subject': day.quarters[index + 1].subject
                        }
                    )
                else:
                    schedule[day].append(
                        {
                                'start_time': day.quarters[index + 1].start_time,
                                'end_time': day.quarters[index + 1].end_time,
                                'subject': day.quarters[index + 1].subject
                        }
                    )


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
                if subject.duration > '120':
                    self.__undo_merge(quarter, quarter + 1)
                    self.quarters[quarter].reset()
                    self.quarters[quarter + 1].reset()
                else:
                    self.quarters[quarter].reset()
                return
        raise 'wrong subject'

    def get_slot(self, subject: Subject) -> bool | tuple | int:
        if subject.duration <= '120':
            for quarter, slot in self.quarters.items():
                slot: Quarter
                if subject.instructors.preferences:
                    start, end = subject.instructors.preferences['start_hour'], subject.instructors.preferences[
                        'end_hour']
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
                if subject.instructors.preferences:
                    start, end = subject.instructors.preferences['start_hour'], subject.instructors.preferences[
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
    def __repr__(self):
        return (f'LectureRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')

    def __str__(self):
        return 'lecture'


class TutorialRoom(Room):
    def __repr__(self):
        return (f'TutorialRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')

    def __str__(self):
        return 'tutorial'


class LaboratoryRoom(Room):
    def __repr__(self):
        return (f'LaboratoryRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')

    def __str__(self):
        return 'laboratory'


class PhysicalTrainingRoom(Room):
    def __repr__(self):
        return (f'BabbleRoom(room_id={self._room_id}, '
                f'capacity={self._capacity}, '
                f'room_name={self._room_name})')

    def __str__(self):
        return 'physical_training'


def get_room(room_id, capacity, room_type, room_name):
    if room_type == 'lecture':
        return LaboratoryRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'tutorial':
        return TutorialRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'laboratory':
        return LaboratoryRoom(room_id=room_id, capacity=capacity, room_name=room_name)
    if room_type == 'physical_training':
        return PhysicalTrainingRoom(room_id=room_id, capacity=capacity, room_name=room_name)
