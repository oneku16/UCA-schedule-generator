from sqlalchemy.ext.asyncio import AsyncSession


class App:
    __slots__ = ('__db',)

    def __init__(self, db: AsyncSession) -> None:
        self.__db: AsyncSession = db
