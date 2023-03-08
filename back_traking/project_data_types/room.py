from room_type import RoomType


class Room:
    __slots__ = '_room_id', '_room_size', '_room_type', '_room_name'

    def __init__(self, room_id: int, room_size: int = 25, room_type: str = 'lecture', room_name=None):
        self._room_id = room_id
        self._room_size = room_size
        self._room_type = RoomType(room_type)
        self._room_name = room_name

    def __str__(self):
        if self._room_name is None:
            return f'{self._room_id}'
        return f'{self._room_id} {self._room_name}'

    @property
    def room_id(self):
        return self._room_id

    @property
    def room_size(self):
        return self._room_size

    @property
    def room_type(self):
        return self._room_type.room_type

    @property
    def room_name(self):
        return self._room_name
