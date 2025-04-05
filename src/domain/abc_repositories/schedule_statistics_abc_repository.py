from abc import ABC, abstractmethod
from typing import Any, Union

from src.domain.models.schedule import ScheduleStatisticsModel


class ABCScheduleStatisticsRepository(ABC):

    @abstractmethod
    async def create_statistics(
            self,
            statistic: dict[str, Any],
    ) -> ScheduleStatisticsModel:
        pass

    @abstractmethod
    async def delete_statistics(
            self,
            statistic_id: int,
    ) -> Union[ScheduleStatisticsModel, None]:
        pass

    @abstractmethod
    async def get_statistics_by_id(
            self,
            statistic_id: int,
    ) -> Union[ScheduleStatisticsModel, None]:
        pass
