from brute_force_3.rooms import Room
from typing import List
from collections import defaultdict


class Serializer:
    __slots__ = ('__rooms',)

    def __init__(self, rooms):
        self.__rooms: List[Room] = rooms

    def room_mode_to_cohort(self):
        cohort_schedule = defaultdict(list)

        for room in self.__rooms:
            for day in room.days:
                for quarter_index, slot in day.quarters.items():
                    if slot.subject:
                        cohort = slot.subject.cohort
                        subject = f'{slot.subject.title}'
                        start_time = slot.start_time
                        end_time = slot.end_time
                        instructor = slot.subject.instructors.primary.instructor_name
                        room_name = f'{room.room_name}: {room.room_id}'
                        cohort_schedule[cohort].append({
                                'subject': subject,
                                'instructor': instructor,
                                'start_time': start_time,
                                'end_time': end_time,
                                'room': room_name,
                                'day': day.day
                        })

        return cohort_schedule
