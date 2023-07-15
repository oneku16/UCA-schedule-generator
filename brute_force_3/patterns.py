from .rooms import LectureRoom, TutorialRoom, LaboratoryRoom, PhysicalTrainingRoom
from .subject import Subject
from typing import List
from config import SUBJECT_PATTERNS


SELECTOR = {
        'lecture': (LectureRoom, TutorialRoom),
        'tutorial': (LectureRoom, TutorialRoom),
        'laboratory': (LaboratoryRoom,),
        'physical_training': (PhysicalTrainingRoom,)
}


class SubjectPattern:
    __slots__ = ('__subjects', 'priority')

    def __init__(self, subject_data):
        self.priority = [0, 0, 0]
        self.__subjects: List[Subject] = self.__create_subjects(**subject_data)

    def __create_subjects(self, cohort, id, instructors, title, patterns) -> List[Subject]:
        subjects = list()
        for subject_type, pattern, index in zip(SUBJECT_PATTERNS, patterns, (2, 1, 0)):
            classes, duration = pattern.values()
            for _ in range(classes):
                self.priority[index] += 1
                subjects.append(
                    Subject(
                        cohort=cohort,
                        id=id,
                        instructors=instructors,
                        title=title,
                        duration=duration,
                        subject_type=self.get_room_type(subject_type)
                    )
                )

        return subjects

    @staticmethod
    def get_room_type(subject_type):
        return SELECTOR.get(subject_type)

    @property
    def subjects(self):
        return self.__subjects

    def __repr__(self):
        return f'SubjectPattern({self.__subjects})'
