from deap import base, creator, tools

from converter import Converter
from config import ROOMS
from brute_force_3.patterns import SubjectPattern
from fyp_2.constraints.subject import Subject
from fyp_2.constraints.room import Room


SELECTOR = {
            'lecture': ('lecture', 'tutorial'),
            'tutorial': ('lecture', 'tutorial'),
            'laboratory': ('laboratory',),
            'physical_training': ('physical_training',)
    }


class GeneticAlgorithm:
    ...


def builder():
    converter = Converter()
    raw_subjects = converter.xlsx_to_json()
    subject_pattern: list[SubjectPattern] = [
        SubjectPattern(subject_data=subject)
        for subject in raw_subjects
    ]
    rooms: list[Room] = [Room(**param) for param in ROOMS]
    subjects: list[Subject] = list()
    for pattern in subject_pattern:
        for subject in pattern.subjects:
            subject.required_rooms = SELECTOR[subject.required_rooms]
            if subject.unique_id.endswith('Physical training'):
                subject.required_rooms = SELECTOR['physical_training']
            subjects.append(
                Subject(
                    subject_id=subject.id,
                    subject_name=subject.title,
                    cohort=subject.cohort,
                    preferred_rooms=subject.required_rooms,
                )
            )
    print(subjects)


if __name__ == "__main__":
    builder()

