from converter import Converter
from brute_force_3.patterns import SubjectPattern
from brute_force_3.rooms import Room, get_room, TutorialRoom
from brute_force_3.schedule_generator import ScheduleGenerator
from brute_force_3.xlsx_generator.table_generator import TableGenerator
from config import ROOMS
from brute_force_3.serializer import Serializer
from pprint import pprint


from deap import algorithms, base, creator, tools
import random
import numpy as np


class GeneticAlgorithmScheduler:
    def __init__(self, rooms: list[Room], subjects: list[SubjectPattern]):
        self.rooms = rooms
        self.subjects = subjects



def main():

    from_converter = Converter().xlsx_to_json()

    subject_patterns: list[SubjectPattern] = [SubjectPattern(subject_data=subject) for subject in from_converter]
    subject_patterns.sort(key=lambda subject: subject.priority, reverse=True)
    rooms: list[Room] = [get_room(**room) for room in ROOMS]

    # pprint(subject_patterns)
    pprint(rooms)

    #
    # schedule_generator = ScheduleGenerator(rooms=rooms, subject_patterns=subject_patterns)
    # schedule_generator.balanced_schedule()
    #
    # serializer = Serializer(rooms=schedule_generator.rooms)
    # schedules = serializer.room_mode_to_cohort()
    # # pprint(from_converter)
    # pprint(dict(schedules))
    # for cohort, schedule in schedules.items():
    #     table = TableGenerator(title=cohort, sequence=schedule)
    #     table.generate_table()


if __name__ == '__main__':
    main()
