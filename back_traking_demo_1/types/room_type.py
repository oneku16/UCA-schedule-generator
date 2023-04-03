from dataclasses import dataclass, field, InitVar


@dataclass(kw_only=True, order=True, frozen=True)
class RoomStructure:
    ...


class LectureRoom(RoomStructure):
    ...


class LaboratoryRoom(RoomStructure):
    ...


