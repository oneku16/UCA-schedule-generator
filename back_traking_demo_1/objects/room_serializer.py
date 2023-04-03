from back_traking_demo_1.types.room_type import LaboratoryRoom, LectureRoom


class RoomSerializer:
    __slots__ = '__room_id', '__room_capacity', '__room_type', '__room_name'

    def __init__(self, room_id: str | int, room_capacity: int, room_type: str, room_name: str):
        self.__room_id = room_id
        self.__room_capacity = room_capacity
        self.__room_type = LaboratoryRoom if room_type.lower() == 'laboratory' else LectureRoom
        self.__room_name = room_name

    @property
    def room_id(self):
        return self.__room_id

    @property
    def room_capacity(self):
        return self.__room_capacity

    @property
    def room_type(self):
        return self.__room_type

    @property
    def room_name(self):
        return self.__room_name
