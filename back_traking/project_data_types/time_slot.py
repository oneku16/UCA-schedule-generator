from collections import deque


class Day:
    __slots__ = '_indexes', '_quarters', '_durations', '_size', '_time_slots'

    def __init__(self):
        self._indexes = deque([0, 1, 2, 3])
        self._quarters = ('first_quarter', 'second_quarter', 'third_quarter', 'fourth_quarter')
        self._durations = {'first_quarter': {'start': '09:00', 'end': '10:30'},
                           'second_quarter': {'start': '11:00', 'end': '12:30'},
                           'third_quarter': {'start': '14:00', 'end': '15:30'},
                           'fourth_quarter': {'start': '16:00', 'end': '17:30'}}
        self._size = len(self._indexes)
        self._time_slots = {index: quarter for index, quarter in zip(self._indexes, self._quarters)}

    @property
    def number_of_slots(self):
        return self._size

    @property
    def is_empty(self):
        return not self._size

    def set_slot(self, preferences=None):
        if preferences is None:
            quarter_index = self._indexes.popleft()
            self._size -= 1
            return self._time_slots[quarter_index]

    def top_slot(self, duration=True):
        if duration:
            start = self._durations[self._time_slots[self._indexes[-1]]]['start']
            end = self._durations[self._time_slots[self._indexes[-1]]]['end']
            # return start, end
            return self._durations[self._time_slots[self._indexes[-1]]]
        return self._time_slots[self._indexes[-1]]

    def bottom_slot(self, duration=True):
        if duration:
            start = self._durations[self._time_slots[self._indexes[0]]]['start']
            end = self._durations[self._time_slots[self._indexes[0]]]['end']
            # return start, end
            return self._durations[self._time_slots[self._indexes[0]]]
        return self._time_slots[self._indexes[0]]


class Monday(Day):
    ...


# class TimeSlot:
#     __slots__ = ''
#
#     def __init__(self):
#         ...


day = Day()
print(day)