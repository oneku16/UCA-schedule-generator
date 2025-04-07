from flet import (
    Page,
    Row,
    Column,
    Container,
)
from flet.core.types import (
    FontWeight,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserResponse
from src.app.components.schedule_view import AdminScheduleView

class AdminComponent(Container):
    def __init__(self, page: Page, user: UserResponse, db: AsyncSession):
        super().__init__()
        self.page = page
        self.user = user
        self.db = db
        self.page.title = "Admin view"
        self.content = Row(
            controls=[
                AdminScheduleView(page=self.page)
            ]
        )
        self.page.update()



