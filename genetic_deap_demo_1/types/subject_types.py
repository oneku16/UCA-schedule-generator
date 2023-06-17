from genetic_deap_demo_1.types.room_types import LectureRoom, TutorialRoom, LaboratoryRoom, SportRoom


class SubjectType:
    ...


class Lecture(SubjectType):
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LectureRoom]


class Tutorial(SubjectType):
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LectureRoom, TutorialRoom]


class Laboratory(SubjectType):
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LaboratoryRoom]


class Sport(SubjectType):
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [SportRoom]


def get_subject_type(subject_type: str) -> Lecture | Tutorial | Laboratory | Sport:
    match subject_type:
        case 'lecture':
            return Lecture()
        case 'tutorial':
            return Tutorial()
        case 'laboratory':
            return Laboratory()
        case 'sport':
            return Sport()
        case _:
            raise 'Wrong subject type'
