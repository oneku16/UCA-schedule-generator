from back_traking.schedule_generator import ScheduleGenerator
from back_traking.project_data_types.subject import Subject
from pprint import pprint
from converter import Converter


def main():
    converter = Converter()
    # pprint(converter.xlsx_to_json())
    subjects = [Subject(**subject) for subject in converter.xlsx_to_json()]
    schedule_generator = ScheduleGenerator(subjects)
    print(subjects[0].subject_id, subjects[0].cohort)
    print(subjects[1].subject_id, subjects[1].cohort)


if __name__ == '__main__':
    main()
