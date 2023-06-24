from dataclasses import dataclass, field
from brute_force_2.room.day import Slots


@dataclass(kw_only=True, slots=True)
class Room:
    room_id: str
    capacity: int
    room_type: str
    room_name: str
    slot: Slots = field(init=False, default_factory=Slots)
