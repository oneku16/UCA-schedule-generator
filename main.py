from back_traking_demo_1.objects.subject import Subject
from converter import Converter
from genetic_deap_demo_1.subjects.subject import Subject
from genetic_deap_demo_1.sorting import sort_subjects
from pprint import pprint
# from brute_force.subject.subject import Subject
from brute_force.tools.priority_queue import HeapQ

from brute_force_2.subject.subject import Subject
from brute_force_2.room.room import Room
from brute_force_2.schedule_generator import ScheduleGenerator
from config import ROOMS, DAYS


def main():
    converter = Converter()
    from_converter = converter.xlsx_to_json()

    pprint(from_converter)
    subjects = sorted([Subject(**item) for item in from_converter],
                      key=lambda item: item.priority, reverse=True)
    rooms = sorted([Room(**room) for room in ROOMS],
                   key=lambda item: (
                       item.room_type != 'bubble',
                       item.capacity),
                   reverse=True)
    rooms_hash = dict()
    for room in ROOMS:
        if room.get('room_type') not in rooms_hash:
            rooms_hash[room.get('room_type')] = list()
        rooms_hash[room.get('room_type')].append(Room(**room))
    # pprint(rooms_hash)
    # print(rooms_hash)
    # print(len(subjects))

    schedule_generator = ScheduleGenerator(rooms=rooms, subjects=subjects)
    schedule_generator.sort_based(rooms_hashed=rooms_hash)

    test_subject = [subject for subject in subjects if subject.id == 'DMNS9142'][-1]

    schedule_generator.test(test_subject)

    # schedule = list(schedule_generator.random_based())

    # temp = list()

    # for room in schedule:
    #     # _temp = list()
    #     print(f'{room.room_name}')
    #     for DAY in DAYS:
    #         try:
    #             room.slot.days.get(DAY).quarters
    #         except AttributeError:
    #             pass
    #         # _temp.append(room)
    #         print(f'{DAY}')
    #         for index, item in room.slot.days.get(DAY).quarters.items():
    #             if not item.status:
    #                 # _temp.append(room)
    #                 h = item.hour
    #                 m = item.minute
    #                 s = item.subject
    #                 print(f'{h}:{m} -> {s.title}')
        # temp.append(_temp)

    # pprint(temp)
    # print([t for t in temp])
    # for room in temp:
    #     for slot in room:
    #         schedule = slot.slot.days
    #         print(slot.room_name)
    #         for day, subjects in schedule.items():
    #             print(day)
    #             for id, quarter in subjects.quarters.items():
    #                 h = quarter.hour
    #                 m = quarter.minute
    #                 s = not quarter.status
    #                 subject = quarter.subject
    #                 if s:
    #                     print(f'{h}:{m} - {subject}')
                    # for _, quarter in quarters.items():
                    #     print(quarter)


if __name__ == '__main__':
    main()
