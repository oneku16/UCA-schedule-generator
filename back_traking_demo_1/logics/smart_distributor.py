from back_traking_demo_1.objects.rooms import Room
from back_traking_demo_1.objects.subject import Subject


class Smart_Distributor:
    __slots__ = '_room', '_subject_pattern'

    def __init__(self, room: Room, subject_pattern: Subject):
        self._room = room
        self._subject_pattern = subject_pattern
