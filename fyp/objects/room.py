from abc import ABC, abstractmethod



class RoomBase(ABC):

    @abstractmethod
    def is_for_subject(self, subject_type: str) -> bool:
        """
        returns true if this room is for subject
        example: regular subject for regular room, lab class/subject for lab, ...
        """
        raise NotImplementedError


class Room(RoomBase):
    def __init__(self, room_id: str, room_name: str, capacity: int, room_type):
        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self.room_type = room_type

    def is_for_subject(self, subject_type: str) -> bool:
        return subject_type == self.room_type
