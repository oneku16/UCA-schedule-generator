from abc import ABC, abstractmethod
from typing import Any, Union

from src.domain.models import ScheduleModel


class ABCScheduleRepository(ABC):

    @abstractmethod
    async def create_schedule(
            self,
            schedule_data: dict[str, Any],
    ) -> ScheduleModel:
        pass

    @abstractmethod
    async def delete_schedule(
            self,
            schedule_id: int,
    ) -> Union[ScheduleModel, None]:
        pass

    @abstractmethod
    async def update_schedule(
            self,
            schedule_data: dict[str, Any],
    ) -> Union[ScheduleModel, None]:
        pass

    @abstractmethod
    async def get_schedule_by_id(
            self,
            schedule_id: int,
    ) -> Union[ScheduleModel, None]:
        pass