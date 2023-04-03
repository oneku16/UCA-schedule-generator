from typing import List, Tuple
from dataclasses import dataclass, field


@dataclass(init=True, kw_only=True, order=True)
class RoomStructure:
    room_id: str
    capacity: int
    room_name: str

class LectureRoom(RoomStructure):
    ...

class LaboratoryRoom(RoomStructure):
    ...

class SportRoom(RoomStructure):
    ...

