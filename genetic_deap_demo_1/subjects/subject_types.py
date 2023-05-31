from genetic_deap_demo_1.rooms.room_types import LectureRoom, TutorialRoom, LaboratoryRoom, SportRoom


class Lecture:
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LectureRoom]


class Tutorial:
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LectureRoom, TutorialRoom]


class Laboratory:
    __slots__ = '__required_rooms'

    def __init__(self):
        self.__required_rooms = [LaboratoryRoom]


class Sport:
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
