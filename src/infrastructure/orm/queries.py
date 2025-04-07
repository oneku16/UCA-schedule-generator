from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models import UserModel


async def get_user_by_id(session: AsyncSession, user_id: int):
    return await session.execute(select(UserModel).where(UserModel.user_id == user_id))


async def get_user_by_email(session: AsyncSession, email: str, password: Optional[str] = None):
    if password is None:
        return await session.execute(select(UserModel).where(UserModel.email == email))
    return await session.execute(
        select(UserModel).where(
            UserModel.email == email, UserModel.password == password
        )
    )