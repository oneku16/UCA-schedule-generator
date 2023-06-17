from typing import List
from genetic_deap_demo_1.subjects.subject import Subject


def sort_subjects(subjects: List[Subject], reverse=True) -> List[Subject]:
    return sorted(subjects, key=lambda subject: (subject.instructors.priority, len(subject.patterns)), reverse=reverse)


def sort_room():
    ...
