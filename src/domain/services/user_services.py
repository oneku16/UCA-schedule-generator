from typing import Union, Optional

from src.domain.abc_repositories.user_abc_repository import ABCUserRepository
from src.domain.models import UserModel
from src.schemas.user import UserCreate, UserResponse


class UserService(ABCUserRepository):

    __slots__ = ('__user_repository',)

    def __init__(self, user_repository: ABCUserRepository):
        self.__user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = await self.__user_repository.create_user(user_data.model_dump())
        return UserResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
        )

    async def delete_user(self, user_id: int) -> Union[UserModel, None]:
        user: Union[UserModel, None] = await self.__user_repository.delete_user(user_id)
        if user is None:
            return None
        return UserResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
        )

    async def is_user_exists(self, email: str) -> bool:
        status: bool = await self.__user_repository.is_user_exists(email=email)
        return status

    async def get_user_by_id(self, user_id: str) -> Union[UserResponse, None]:
        user = await self.__user_repository.get_user_by_id(user_id=user_id)
        if not user:
            return None
        return UserResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
        )

    async def get_user_by_email(self, email: str, password: Optional[str] = None) -> Union[UserResponse, None]:
        user = await self.__user_repository.get_user_by_email(email=email)
        if not user:
            return None
        return UserResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
        )
