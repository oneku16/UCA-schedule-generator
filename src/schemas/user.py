from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(None, example="john_doe")
    email: EmailStr  = Field(None, example="user@example.com")
    password: str = Field(None, example="securepassword123")
    role: Optional[str] = Field(None, example="admin")

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True
