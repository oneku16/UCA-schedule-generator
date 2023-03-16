from back_traking.schedule_generator import ScheduleGenerator
from back_traking.data_types.json_to_object import JSONToObject
from converter import Converter
from pprint import pprint

def main():

    converter = Converter()
    subjects = [JSONToObject(**subject) for subject in converter.xlsx_to_json()]
    schedule_generator = ScheduleGenerator(subjects)
    schedule_generator.test()


if __name__ == '__main__':
    main()
