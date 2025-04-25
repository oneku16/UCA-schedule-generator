from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models import UserModel, ScheduleModel


async def get_user_by_id(session: AsyncSession, user_id: int):
    return await session.execute(select(UserModel).where(UserModel.user_id == user_id))


async def get_user_by_email(session: AsyncSession, email: str, password: Optional[str] = None):
    if password is None:
        return await session.execute(
            select(UserModel).where(
                UserModel.email == email
            )
        )
    return await session.execute(
        select(UserModel).where(
            UserModel.email == email, UserModel.password == password
        )
    )

async def get_schedule(
        session: AsyncSession,
        schedule_id: Optional[int] = None,
        schedule_name: Optional[str] = None
):
    if schedule_id is not None:
        statement = ScheduleModel.schedule_id == schedule_id
    elif schedule_name is not None:
        statement = ScheduleModel.schedule_name == schedule_name
    else:
        raise ValueError("schedule_id or schedule_name must be provided")
    return await session.execute(select(ScheduleModel).where(statement))
