from flet import Page, app

from src.infrastructure.database import create_db_and_tables, get_db_context
from src.app.components.auth_component import AuthenticationView


async def main(page: Page):
    await create_db_and_tables()

    async with get_db_context() as db:
        page.clean()
        authentication_view = AuthenticationView(page=page, db=db)
        page.add(authentication_view)
        page.update()


if __name__ == '__main__':
    app(target=main)
