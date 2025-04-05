from asyncio import run

from src.infrastructure.database import create_db_and_tables, get_db_context
from src.schemas.user import UserCreate
from src.infrastructure.orm.user_orm_repository import SQLUserRepository
from src.domain.services.user_services import UserService


user = UserCreate(
    username='eku',
    email='eku.ulanov@yandex.com',
    password='admin',
    role='admin'
)


async def main():
    await create_db_and_tables()

    async with get_db_context() as db:
        user_repository = SQLUserRepository(db=db)

        if await user_repository.is_user_exists(email=user.email):
            print("User already exists.")
            return

        service = UserService(user_repository)
        new_user = await service.create_user(user)
        print(f"User created: {new_user}")


if __name__ == '__main__':
    run(main())


