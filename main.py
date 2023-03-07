from back_traking.schedule_generator import ScheduleGenerator
from back_traking.project_data_types.subject import Subject
from converter import Converter


def main():
    converter = Converter()
    subjects = [Subject(**subject) for subject in converter.xlsx_to_json()]
    schedule_generator = ScheduleGenerator(subjects)
    print((subjects[0]))


if __name__ == '__main__':
    main()
