from back_traking_demo_1.schedule_generator import ScheduleGenerator
from back_traking_demo_1.objects.subject import Subject
from converter import Converter
from pprint import pprint
from genetic_deap_demo_1.rooms.room import get_room_instance
from genetic_deap_demo_1.bases.subject import Subject
from genetic_deap_demo_1.subjects.subject_types import Lecture


def main():

    converter = Converter()
    # test = [Subject(**item) for item in subjects[:3]]
    subjects = [Subject(**subject) for subject in converter.xlsx_to_json()]
    pprint([[pattern.subject_type is Lecture for pattern in subject.patterns] for subject in subjects])
    # # schedule_generator = ScheduleGenerator(subjects)
    # # schedule_generator.test()
    ...


if __name__ == '__main__':
    main()
