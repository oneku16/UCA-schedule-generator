from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.core.config import database_settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(database_settings.url, pool_recycle=900, pool_size=100, max_overflow=3)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# ✅ Table creation
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[Any, Any]:
    async with async_session_maker() as db:
        yield db

