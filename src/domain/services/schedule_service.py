from typing import Union, Any

from src.domain.abc_repositories import ABCScheduleRepository
from src.domain.models import ScheduleModel


class ScheduleService(ABCScheduleRepository):

    __slots__ = ('__repository',)

    def __init__(self, repository: ABCScheduleRepository) -> None:
        self.__repository = repository

    async def create_schedule(self, schedule_data: dict[str, Any]) -> ScheduleModel:
        schedule = await self.__repository.create_schedule(schedule_data)
        return schedule

    async def delete_schedule(self, schedule_id: int) -> Union[ScheduleModel, None]:
        schedule = await self.__repository.delete_schedule(schedule_id)
        return schedule

    async def update_schedule(self, schedule_data: dict[str, Any]) -> Union[ScheduleModel, None]:
        schedule = await self.__repository.update_schedule(schedule_data)
        return schedule

    async def get_schedule_by_id(self, schedule_id: int) -> Union[ScheduleModel, None]:
        schedule = await self.__repository.get_schedule_by_id(schedule_id=schedule_id)
        return schedule

    async def get_schedule_by_name(self, schedule_name: str) -> Union[ScheduleModel, None]:
        schedule = await self.__repository.get_schedule_by_name(schedule_name=schedule_name)
        return schedule
