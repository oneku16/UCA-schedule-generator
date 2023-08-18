import numpy as np

from brute_force_3.rooms import Room, TutorialRoom, LaboratoryRoom, LectureRoom, PhysicalTrainingRoom
from brute_force_3.patterns import SubjectPattern
from brute_force_3.subject import Subject, Tutorial, Lecture, Laboratory
from brute_force_3.balace import Balancer

from random import shuffle, choice
from typing import List
from sys import setrecursionlimit

setrecursionlimit(100_000)


class ScheduleGenerator:
    __slots__ = ('rooms', 'subject_patterns', 'used_subjects', 'used_rooms')

    def __init__(self, *, rooms, subject_patterns):
        self.rooms: List[Room] = rooms
        # shuffle(self.rooms)
        self.subject_patterns: List[SubjectPattern] = subject_patterns

    def __get_potential_slots(self, subject: Subject):
        potential_rooms = list()
        for room_index, room in enumerate(self.rooms):
            slots = room.get_slots_for_subject(subject=subject)
            if slots:
                potential_rooms.append([room_index, slots])
        return potential_rooms

    @staticmethod
    def __is_mother_room(room: Room, subject: Subject) -> bool:
        for day in room.days:
            for quarter_index, slot in day.quarters.items():
                if slot.status and slot.subject.unique_id == subject.unique_id:
                    return True
        return False

    def __get_preferred_rooms(self, subject: Subject):
        preferred_rooms = list()
        for room_id in subject.instructors.primary.preferences.rooms:
            for room_index, room in enumerate(self.rooms):
                if room_id == room.room_id:
                    preferred_rooms.append(room_index)
        return preferred_rooms

    def __get_schedule_map(self, unique_id: str | int, room_index: int = None) -> np.ndarray:
        schedule_map = np.zeros((4, 5))
        if room_index is not None:
            for day_index, day in enumerate(self.rooms[room_index].days):
                for slot_index, slot in day.quarters.items():
                    if slot.status and slot.subject.unique_id != unique_id:
                        if day.is_merged(slot_index=slot_index - 1):
                            first, second = day.is_merged(slot_index=slot_index - 1)
                            schedule_map[second][day_index] = np.nan
                            schedule_map[first][day_index] = np.nan
                        else:
                            schedule_map[slot_index - 1][day_index] = np.nan

        for room in self.rooms:
            for day_index, day in enumerate(room.days):
                for slot_index, slot in day.quarters.items():
                    if slot.status:
                        if slot.subject.unique_id == unique_id:
                            if day.is_merged(slot_index=slot_index - 1):
                                first, second = day.is_merged(slot_index=slot_index - 1)
                                schedule_map[second][day_index] = 0.5
                                schedule_map[first][day_index] = 0.5
                            else:
                                schedule_map[slot_index - 1][day_index] = 1
        return schedule_map

    @staticmethod
    def __is_tutorial_subject(subject: Subject) -> bool:
        return isinstance(subject, Tutorial)

    @staticmethod
    def __is_lecture_subject(subject: Subject) -> bool:
        return isinstance(subject, Lecture)

    def __set_tutorial_subject(self, subject: Subject) -> bool:
        preferred_rooms = self.__get_preferred_rooms(subject=subject)

        for room_index in preferred_rooms:
            if self.rooms[room_index].days[-1].get_slot(subject):
                _, slots = self.rooms[room_index].days[-1].slots_for_subject(subject=subject, _status=False)
                self.rooms[room_index].days[-1].set_subject(slots=slots[0], subject=subject)
                return True
        else:
            for room_index in range(len(self.rooms)):
                if isinstance(self.rooms[room_index], LectureRoom) and self.rooms[room_index].days[-1].slots_for_subject(subject):
                    status, slots = self.rooms[room_index].days[-1].slots_for_subject(subject=subject, _status=False)
                    self.rooms[room_index].days[-1].set_subject(slot=slots[0], subject=subject)
                    return True
        raise 'Not Found'

    def __get_slot(self, subject_unique_id, room_index):
        room_map = self.__get_schedule_map(subject_unique_id, room_index)
        balanced = Balancer(room_map=room_map)
        return balanced.get_slot

    def __set_lecture_subject(self, subject: Subject, day_slot=None) -> bool:
        preferred_rooms = self.__get_preferred_rooms(subject=subject)
        if day_slot is None:
            day_slot = self.__get_best_day(subject.unique_id)

        for room_index in preferred_rooms:
            if self.rooms[room_index].days[day_slot].get_slot(subject=subject):
                # _, slots = self.rooms[room_index].days[day_slot].slots_for_subject(subject=subject, _status=False)
                # self.rooms[room_index].days[day_slot].set_subject(slot=slots[0], subject=subject)
                quarter_index, day_index = self.__get_slot(subject_unique_id=subject.unique_id, room_index=room_index)
                self.rooms[room_index].days[day_index].set_subject(slot=quarter_index + 1, subject=subject)
                return True
        else:
            for room_index in range(len(self.rooms)):
                if isinstance(self.rooms[room_index], (LectureRoom,)):
                    if self.rooms[room_index].days[day_slot].slots_for_subject(subject):
                        # _, slots = self.rooms[room_index].days[day_slot].slots_for_subject(subject=subject, _status=False)
                        # self.rooms[room_index].days[day_slot].set_subject(slot=slots[0], subject=subject)
                        quarter_index, day_index = self.__get_slot(subject_unique_id=subject.unique_id, room_index=room_index)
                        self.rooms[room_index].days[day_index].set_subject(slot=quarter_index + 1, subject=subject)
                        return True

        for room_index in range(len(self.rooms)):
            if isinstance(self.rooms[room_index], (LectureRoom,)) and self.rooms[room_index].is_slot_available():
                for day_slot, day in enumerate(self.rooms[room_index].days):
                    if day.slots_for_subject(subject=subject):
                        # _, slots = self.rooms[room_index].days[day_slot].slots_for_subject(subject=subject, _status=False)
                        # self.rooms[room_index].days[day_slot].set_subject(slot=slots[0], subject=subject)
                        quarter_index, day_index = self.__get_slot(subject_unique_id=subject.unique_id, room_index=room_index)
                        self.rooms[room_index].days[day_index].set_subject(slot=quarter_index + 1, subject=subject)
                        return True

    def __get_best_day(self, unique_id: str) -> int:
        schedule_map = self.__get_schedule_map(unique_id=unique_id)
        column_sum = np.sum(a=schedule_map, axis=0)
        day_index = choice((0, 4))
        if column_sum.sum() % column_sum.size:
            center_of_mass = np.average(np.arange(column_sum.size), weights=column_sum)
            day_index = int((column_sum.size - 1) - int(round(center_of_mass)))
        return day_index

    def __place_subject(self, subject_pattern_index: int, subject_index: int, preferred_rooms: List[int] = None) -> None:
        subject = self.subject_patterns[subject_pattern_index].subjects[subject_index]
        if preferred_rooms is None:
            if self.__is_tutorial_subject(subject=subject):
                if self.__set_tutorial_subject(subject=subject):
                    self.subject_patterns[subject_pattern_index].subjects[subject_index].subject_status = False
            if self.__is_lecture_subject(subject=subject):
                if self.__set_lecture_subject(subject=subject):
                    self.subject_patterns[subject_pattern_index].subjects[subject_index].subject_status = False

    def __separate(self, *subject_type) -> List[List[int]]:
        rooms = list()
        for subject_pattern_index in range(len(self.subject_patterns)):
            for subject_index in range(len(self.subject_patterns[subject_pattern_index].subjects)):
                if isinstance(self.subject_patterns[subject_pattern_index].subjects[subject_index], subject_type):
                    rooms.append([subject_pattern_index, subject_index])
        return rooms

    def balanced_schedule(self):
        schedule = dict()

        for subject_pattern_index, subject_index in self.__separate(Tutorial):
            self.__place_subject(subject_pattern_index=subject_pattern_index, subject_index=subject_index)

        for subject_pattern_index, subject_index in self.__separate(Lecture):
            self.__place_subject(subject_pattern_index=subject_pattern_index, subject_index=subject_index)

    def empty_rooms(self, subject: Subject):
        print(subject, type(subject))
        for room in self.rooms:
            if room.is_slot_available():
                print(room)

    def subjects_no_slot(self):
        for subject_pattern in self.subject_patterns:
            for subject in subject_pattern.subjects:
                if subject.subject_status:
                    yield subject


