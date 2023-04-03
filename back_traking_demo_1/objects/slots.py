from back_traking_demo_1.configs import DAYS
from back_traking_demo_1.objects.subject_pattern_type import SubjectPatternType
from back_traking_demo_1.project_exceptions.time_slot_exceptions import NoSlots, OverFlowSlots
from typing import List


class Slots:
    __slots__ = '_days'

    class __Day:
        __slots__ = '_day', '_quarters', '_quarters_dict', '_durations', '_size'

        def __init__(self, day):
            self._day = day
            self._quarters = ('first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter')
            self._quarters_dict = {quarter: True for quarter in self._quarters}
            self._durations = {'first_quarter': {'start_time': '09:00', 'end_time': '10:30'},
                               'second_quarter': {'start_time': '11:00', 'end_time': '12:30'},
                               'third_quarter': {'start_time': '14:00', 'end_time': '15:30'},
                               'fourth_quarter': {'start_time': '16:00', 'end_time': '17:30'}}
            self._size = len(self._quarters)

        @property
        def day(self):
            return self._day

        @property
        def number_of_slots(self):
            return self._size

        @property
        def is_empty(self):
            return not self._size == 0

        @property
        def is_full(self):
            return self._size == 0

        def is_possible(self, add=False):
            if add:
                return True if self._size < 4 else False
            return True if self._size >= 1 else False

        @property
        def slot_for_lecture(self):
            return self._size >= 1

        @property
        def slot_for_laboratory(self):
            return self._size >= 2

        @property
        def __get_top(self):
            quarter_dict = tuple(self._quarters_dict.values())
            for index in range(len(self._quarters) - 1, -1, -1):
                if quarter_dict[index]:
                    return index

        @property
        def __get_bottom(self):
            for index, value in enumerate(self._quarters_dict.values()):
                if value:
                    return index

        def reserve_slot(self, subject: SubjectPatternType, preferences=None):
            if not self.is_empty:
                raise NoSlots
            if preferences is None:
                print(subject.name)
            if self.is_full:
                raise NoSlots
            self._size -= 1

        def undo_reservation(self, subject: SubjectPatternType, slot: tuple[str | tuple[str, str]]):
            if self.is_full:
                raise OverFlowSlots

    def __init__(self):
        self._days = self.__generate_days()

    @property
    def days(self):
        return self._days

    @classmethod
    def __generate_days(cls) -> List[__Day]:
        def _wrapper():
            for day in DAYS:
                yield cls.__Day(day)

        return list(_wrapper())
