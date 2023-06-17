class SuperRoom:
    __slots__ = ('_room_id', '_room_capacity', '_room_name', '_days')

    def __init__(self, room_id, room_capacity, room_name):
        self._room_id = room_id
        self._room_capacity = room_capacity
        self._room_name = room_name
        self._days = []

    def add_subject(self):
        ...

    def remove_subject(self):
        ...


class LectureTutorial(SuperRoom):
    def __init__(self, room_id, room_capacity, room_name):
        super().__init__(room_id, room_capacity, room_name)


class LectureTutorialLaboratory(LectureTutorial):
    def __init__(self, room_id, room_capacity, room_name):
        super().__init__(room_id, room_capacity, room_name)


class Sport(SuperRoom):
    def __init__(self, room_id, room_capacity, room_name):
        super().__init__(room_id, room_capacity, room_name)


def get_room_instance(room_id, room_capacity, room_name, room_type) -> LectureTutorial | LectureTutorialLaboratory | Sport:
    if room_type in ('lecture', 'tutorial'):
        return LectureTutorial(room_id, room_capacity, room_name)
    elif room_type == 'laboratory':
        return LectureTutorialLaboratory(room_id, room_capacity, room_name)
    elif room_type == 'bubble':
        return Sport(room_id, room_capacity, room_name)
    raise 'Wrong room type'
