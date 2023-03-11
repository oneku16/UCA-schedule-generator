from back_traking.schedule_generator import ScheduleGenerator
from back_traking.project_data_types.subject import Subject
from converter import Converter
from time import perf_counter


def main():

    start_time = perf_counter()
    converter = Converter()
    subjects = [Subject(**subject) for subject in converter.xlsx_to_json()]
    subjects.sort(key=lambda subject: (subject.subject_pattern.counter, [pattern.number_of_classes for pattern in subject.subject_pattern.patterns]), reverse=True)


if __name__ == '__main__':
    main()
