from typing import Optional, Union, Any, overload

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc_repositories import ABCUserRepository
from src.domain.models import UserModel
from src.infrastructure.orm.queries import get_user_by_email, get_user_by_id


class SQLUserRepository(ABCUserRepository):

    __slots__ = ('__db',)

    def __init__(self, db: AsyncSession):
        self.__db = db

    async def create_user(self, user_data: dict[str, Any]) -> UserModel:
        user = UserModel(**user_data)
        self.__db.add(user)
        await self.__db.commit()
        await self.__db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> Union[UserModel, None]:
        pass

    async def is_user_exists(self, email: str) -> bool:
        async with self.__db as session:
            user: Optional[UserModel] = (
                await get_user_by_email(
                    session=session,
                    email=email,
                )
            ).scalar_one_or_none()
        return True if user else False

    async def get_user_by_id(self, user_id: int) -> Union[UserModel, None]:
        async with self.__db as session:
            user: Optional[UserModel] = await get_user_by_id(session=session, user_id=user_id)
        return user

    async def get_user_by_email(self, email: str, password: Optional[str] = None) -> UserModel | None:
        async with self.__db as session:
            user: Optional[UserModel] = (
                await get_user_by_email(session=session, email=email, password=password)
            ).scalar_one_or_none()
        return user
