from abc import ABC, abstractmethod
from typing import Any, Union, Optional

from src.domain.models.user import UserModel


class ABCUserRepository(ABC):

    @abstractmethod
    async def create_user(
            self,
            user_data: dict[str, Any],
    ) -> UserModel:
        pass

    @abstractmethod
    async def delete_user(
            self,
            user_id: int,
    ) -> Union[UserModel, None]:
        pass

    @abstractmethod
    async def is_user_exists(
            self,
            email: str,
    ) -> bool:
        pass

    @abstractmethod
    async def get_user_by_id(
            self,
            user_id: str,
    ) -> Union[UserModel, None]:
        pass

    @abstractmethod
    async def get_user_by_email(
            self,
            email: str,
            password: Optional[str] = None,
    ) -> Union[UserModel, None]:
        pass
