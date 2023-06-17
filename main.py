from back_traking_demo_1.objects.subject import Subject
from converter import Converter
from genetic_deap_demo_1.subjects.subject import Subject
from genetic_deap_demo_1.sorting import sort_subjects
from pprint import pprint
from brute_force.subject.subject import Subject
from brute_force.tools.priority_queue import HeapQ


def main():

    converter = Converter()

    from_converter = converter.xlsx_to_json()
    temp = [Subject(**item) for item in from_converter]

    subjects = HeapQ()

    for subject in temp:
        # print(subject.priority, subject)
        # print(subjects)
        subjects.add(subject.priority, subject)
    # pprint(from_converter)
    # subjects.sort(key=lambda item: item.priority, reverse=True)
    # for subject in subjects:
    #     print(subject.patterns)
        # for pattern in subject.patterns:

    # subjects = sort_subjects([Subject(**subject) for subject in converter.xlsx_to_json()])
    # pprint([[pattern.subject_type is Lecture for pattern in subject.patterns] for subject in subjects])
    # # schedule_generator = ScheduleGenerator(subjects)
    # # schedule_generator.test()





if __name__ == '__main__':
    main()
