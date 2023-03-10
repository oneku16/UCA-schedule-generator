from collections import deque


class Day:
    __slots__ = '_first_quarter', '_second_quarter', '_third_quarter', '_fourth_quarter', '_slots', '_quarters', '_size'

    def __init__(self):
        self._first_quarter = False
        self._second_quarter = False
        self._third_quarter = False
        self._fourth_quarter = False
        self._slots = deque(['first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter'])
        self._quarters = {'first_quarter': {'start_time': '09:00', 'end_time': '10:30'},
                          'second_quarter': {'start_time': '11:00', 'end_time': '12:30'},
                          'third_quarter': {'start_time': '14:00', 'end_time': '15:30'},
                          'fourth_quarter': {'start_time': '16:00', 'end_time': '17:30'}
                          }
        self._size = len(self._slots)

    def top_quarter(self):
        return self._slots[-1] if self._slots else False

    def bottom_quarter(self):
        return self._slots[0] if self._slots else False

    def set_quarter(self, quarter=None, instructor_preference=None):
        self._size -= 1
        if quarter is None:
            quarter = self.bottom_quarter()
            self._slots.popleft()
        else:
            pass

    @property
    def is_possible(self):
        return self._size != 0

    @property
    def is_first_quarter(self):
        return self._first_quarter

    @property
    def is_second_quarter(self):
        return self._second_quarter

    @property
    def is_third_quarter(self):
        return self._third_quarter

    @property
    def is_fourth_quarter(self):
        return self._fourth_quarter


class Monday(Day):
    ...


class TimeSlot:
    __slots__ = ''

    def __init__(self):
        ...
