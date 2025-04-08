from __future__ import annotations

from typing import Any
from flet import (
    Page,
    Column,
    ElevatedButton,
    TextField,
    Text,
    SnackBar,
    Row,
)
from flet.core.types import FontWeight, MainAxisAlignment, CrossAxisAlignment
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.orm import SQLUserRepository
from src.schemas import UserCreate, UserResponse
from src.app.components.admin_component import AdminComponent
from src.app.components.schedule_view import AdminScheduleView


class LoginView(Column):
    def __init__(self, page: Page, parent: AuthenticationView, db: AsyncSession) -> None:
        super().__init__()
        self.page = page
        self.__parent = parent
        self.__db = db
        self.email = TextField(value='eku.ulanov@yandex.com', label="Email", width=300)
        self.password = TextField(value='admin', label="Password", password=True, width=300)
        self.alignment = MainAxisAlignment.CENTER,
        self.horizontal_alignment = CrossAxisAlignment.CENTER,
        self.controls=[
            Text(
                value="Login",
                size=24,
                weight=FontWeight.BOLD,
            ),
            self.email,
            self.password,
            Row(
                controls=[
                    ElevatedButton(
                        text="Log In",
                        on_click=self.handle_login,
                    ),
                    ElevatedButton(
                        text="Sign Up",
                        on_click=self.handle_signup,
                    ),
                ],
            )
        ]

    async def handle_login(self, event):
        user_repository = SQLUserRepository(db=self.__db)
        user_model = await user_repository.get_user_by_email(email=self.email.value, password=self.password.value)
        if user_model:
            snack_bar = SnackBar(Text("Login Successful!"), bgcolor="green")
            snack_bar.open = True
            self.page.open(snack_bar)
            self.page.update()
            user = UserResponse.model_validate(user_model)
            if user.role == 'admin':
                self.page.clean()
                self.page.add(AdminComponent(page=self.page, user=user, db=self.__db))
                self.page.update()
            else:
                ...
        else:
            snack_bar = SnackBar(Text("Login Failed!"), bgcolor="red")
            snack_bar.open = True
            self.page.open(snack_bar)
            self.page.update()

    def handle_signup(self, event):
        self.__parent.signup_view()


class SignUpView(Column):
    def __init__(self, page: Page, parent: AuthenticationView, db: AsyncSession) -> None:
        super().__init__()
        self.page = page
        self.__parent = parent
        self.__db = db
        self.username = TextField(label='username', width=300)
        self.username = TextField(label="Username", width=300)
        self.email = TextField(label="Email", width=300)
        self.password = TextField(label="Password", password=True, width=300)
        self.signup_button = ElevatedButton("Sign Up", on_click=self.handle_signup)
        self.back_button = ElevatedButton("Back to Login", on_click=self.handle_back)
        self.controls = [
            Text(
                value="Sign Up",
                size=24,
                weight=FontWeight.BOLD,
            ),
            self.username,
            self.email,
            self.password,
            Row(
                controls=[
                    self.signup_button,
                    self.back_button,
                ],
                alignment=MainAxisAlignment.START)
        ]
        self.alignment = MainAxisAlignment.START
        self.horizontal_alignment = CrossAxisAlignment.START

    async def get_user_data(self) -> dict[str, Any]:
        user_data = {
            'username': self.username.value,
            'email': self.email.value,
            'password': self.password.value,
        }
        return user_data

    async def handle_signup(self, event):
        user_data = await self.get_user_data()

        user_repository = SQLUserRepository(db=self.__db)
        is_user_exists = await user_repository.is_user_exists(email=self.email.value)
        if is_user_exists:
            snack_bar = SnackBar(Text("Email already exists."), bgcolor="red")
            snack_bar.open = True
            self.page.open(snack_bar)
            self.page.update()
        else:
            try:
                user_create = UserCreate.model_validate(user_data)
                snack_bar = SnackBar(Text("Signup successful!"), bgcolor="green")
                await user_repository.create_user(
                    user_data=user_create.model_dump()
                )
                self.__parent.login_view()
            except ValidationError as e:
                snack_bar = SnackBar(Text("Invalid fields: " + str(e)), bgcolor="red")

            snack_bar.open = True
            self.page.open(snack_bar)
            self.page.update()

    def handle_back(self, event):
        self.__parent.login_view()


class AuthenticationView(Column):
    def __init__(self, page: Page, db: AsyncSession):
        super().__init__()
        self.page = page
        self.__db = db
        self.width = 1920
        self.height = 1080
        self.login_view()

    def login_view(self) -> None:
        self.page.clean()
        self.page.add(LoginView(page=self.page, parent=self, db=self.__db))
        self.page.update()

    def signup_view(self) -> None:
        self.page.clean()
        self.page.add(SignUpView(page=self.page, parent=self, db=self.__db))
        self.page.update()
