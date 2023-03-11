from typing import Tuple, Any
from back_traking.project_exceptions.time_slot_exceptions import NoSlots, OverFlowSlots


class Day:
    __slots__ = '_quarters', '_quarters_dict', '_durations', '_size'

    def __init__(self):
        self._quarters = ('first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter')
        self._quarters_dict = {quarter: True for quarter in self._quarters}
        self._durations = {'first_quarter': {'start_time': '09:00', 'end_time': '10:30'},
                           'second_quarter': {'start_time': '11:00', 'end_time': '12:30'},
                           'third_quarter': {'start_time': '14:00', 'end_time': '15:30'},
                           'fourth_quarter': {'start_time': '16:00', 'end_time': '17:30'}}
        self._size = len(self._quarters)

    @property
    def number_of_slots(self):
        return self._size

    @property
    def is_empty(self):
        return self._size == 0

    @property
    def is_available(self):
        return self._size >= 1

    @property
    def is_full(self):
        return self._size == len(self._quarters)

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

    def get_slot(self, bottom=True, class_call=False, only_duration: bool = True) -> tuple[int, Any] | Any:
        if self.is_empty:
            raise NoSlots
        index = self.__get_bottom if bottom else self.__get_top
        if class_call:
            return self._quarters[index], self._durations[self._quarters[index]]
        if only_duration:
            return self._durations[self._quarters[index]]
        return self._quarters[index]

    def reserve_slot(self, preferences=None):
        if self.is_empty:
            raise NoSlots
        if preferences is None:
            quarter, time = self.get_slot(class_call=True)
            self._size -= 1
            self._quarters_dict[quarter] = False
            return quarter, time

    def undo_reservation(self, quarter):
        if self.is_full:
            raise OverFlowSlots
        self._size += 1
        self._quarters_dict[quarter] = True

class Monday(Day):
    ...


class Tuesday(Day):
    ...


class Wednesday(Day):
    ...


class Thursday(Day):
    ...


class Friday(Day):
    ...


class TimeSlot:
    __slots__ = ''

    def __init__(self):
        ...

