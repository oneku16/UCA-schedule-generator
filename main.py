from back_traking_demo_1.schedule_generator import ScheduleGenerator
from back_traking_demo_1.objects.subject import Subject
from converter import Converter
from pprint import pprint

def main():

    converter = Converter()
    for item in converter.xlsx_to_json():
        print(item)
    # subjects = [Subject(**subject) for subject in converter.xlsx_to_json()]
    # schedule_generator = ScheduleGenerator(subjects)
    # schedule_generator.test()


if __name__ == '__main__':
    main()
