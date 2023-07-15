from typing import List

from converter import Converter
from brute_force_3.patterns import SubjectPattern
from brute_force_3.rooms import Room, get_room
from config import ROOMS
from pprint import pprint


def from_json():
    with open('subjects.json', 'r') as file:
        return file.read()


def main():
    from_converter = Converter().xlsx_to_json()

    subject_patterns: List[SubjectPattern] = [SubjectPattern(subject_data=subject) for subject in from_converter]
    subject_patterns.sort(key=lambda subject: subject.priority, reverse=True)
    subject = subject_patterns[0]

    rooms: List[Room] = [get_room(**room) for room in ROOMS]
    room = rooms[0]

    


    # pprint(rooms)


if __name__ == '__main__':
    main()
