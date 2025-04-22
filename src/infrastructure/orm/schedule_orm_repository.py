from typing import Optional, Union, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc_repositories import ABCScheduleRepository
from src.domain.models import ScheduleModel
from src.infrastructure.orm.queries import get_schedule_by_id


class SQLScheduleRepository(ABCScheduleRepository):
    __slots__ = ('__db',)

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_schedule(self, schedule_data: dict[str, Any]) -> ScheduleModel:
        schedule = ScheduleModel(**schedule_data)
        self.__db.add(schedule)
        await self.__db.commit()
        await self.__db.refresh(schedule)
        return schedule

    async def delete_schedule(self, schedule_id: int) -> Union[ScheduleModel, None]:
        async with self.__db as session:
            schedule: Optional[ScheduleModel] = (
                await get_schedule_by_id(session, schedule_id)
            ).scalar_one_or_none()
            if schedule:
                await self.__db.delete(schedule)
                await self.__db.commit()
        return schedule

    async def update_schedule(self, schedule_data: dict[str, Any]) -> Union[ScheduleModel, None]:
        async with self.__db as session:
            schedule: Optional[ScheduleModel] = (
                await get_schedule_by_id(session, schedule_data.get('schedule_id'))
            ).scalar_one_or_none()
            for key, item in schedule_data.items():
                setattr(schedule, key, item)
            await self.__db.commit()
            await self.__db.refresh(schedule)
        return schedule

    async def get_schedule_by_id(self, schedule_id: int) -> Union[ScheduleModel, None]:
        async with self.__db as session:
            schedule: Optional[ScheduleModel] = (
                await get_schedule_by_id(session, schedule_id)
            ).scalar_one_or_none()
        return schedule
