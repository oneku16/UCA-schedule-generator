from collections import defaultdict
from datetime import datetime
from pprint import pprint
from time import perf_counter

from consts import ROOMS

from schedule.converter import Converter

from schedule.schedule_generator.constraints import SubjectPattern, Subject, Room, Instructor
from schedule.schedule_generator.genetic_algorithm.genetic_algorithm import GeneticAlgorithm


def build():

    from_converter = Converter().xlsx_to_json()

    subject_patterns: list[SubjectPattern] = [SubjectPattern(subject_data=subject) for subject in from_converter]
    subjects: list[Subject] = [subject for pattern in subject_patterns for subject in pattern.subjects]
    rooms: list[Room] = [Room(**room) for room in ROOMS]

    genetic_algorithm = GeneticAlgorithm(subjects=subjects, rooms=rooms, instructors=[None] * 28)

    start_time = perf_counter()
    res = genetic_algorithm.run()
    end_time = perf_counter()
    pprint(res)
    print("Time taken: ", end_time - start_time)

    schedule_data = defaultdict(list)

    for subject, slot, room, instructor in res:
        schedule_data[subject.cohort].append(
            {
                "subject": subject.subject_name,
                "start_time": datetime.strptime(slot.start_time, "%H:%M").strftime("%H:%M"),
                "end_time": datetime.strptime(slot.end_time, "%H:%M").strftime("%H:%M"),
                "room": room.room_id,
                "day": slot.week_day,
            }
        )

    return schedule_data
