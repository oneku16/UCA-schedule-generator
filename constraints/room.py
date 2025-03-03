class Room:
    __slots__ = (
        "room_id",
        "capacity",
        "room_type",
        "extra_constraints",
    )
    def __init__(
            self,
            room_id: str,
            capacity: int,
            room_type: str,
            **extra_constraints,
    ):
        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.extra_constraints = extra_constraints

    def __repr__(self):
        return f'Room(id={self.room_id}, type={self.room_type})'
