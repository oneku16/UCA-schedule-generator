from pydantic import BaseModel
from typing import Any


class ScheduleCreate(BaseModel):
    schedule_name: str
    owner_id: int

    class Config:
        from_attributes = True


class ScheduleResponse(BaseModel):
    schedule_id: int
    schedule_name: str
    data: dict[str, Any]
    owner_id: int
    rating: float = 5.0

    class Config:
        from_attributes = True


class ScheduleUpdate(BaseModel):
    owner_id: int
    schedule_id: int
    schedule_name: str
    data: dict[str, Any]
    rating: float

    class Config:
        from_attributes = True
