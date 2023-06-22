from back_traking_demo_1.objects.subject import Subject
from converter import Converter
from genetic_deap_demo_1.subjects.subject import Subject
from genetic_deap_demo_1.sorting import sort_subjects
from pprint import pprint
# from brute_force.subject.subject import Subject
from brute_force.tools.priority_queue import HeapQ
from brute_force_2.subject.subject import Subject


def main():
    converter = Converter()
    from_converter = converter.xlsx_to_json()
    subjects = [Subject(**item) for item in from_converter]

    for subject in subjects:
        print(subject.priority)


if __name__ == '__main__':
    main()
