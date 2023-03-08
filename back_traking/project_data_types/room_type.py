class Lecture:
    ...

class Laboratory:
    ...

class Bubble:
    ...

class RoomType:
    __slots__ = '_room_type', '_options'

    def __init__(self, room_type: str):
        self._room_type = room_type
        self._options = {'lecture': Lecture, 'laboratory': Laboratory, 'bubble': Bubble}

    @property
    def room_type(self):
        return self._options.get(self._room_type)
