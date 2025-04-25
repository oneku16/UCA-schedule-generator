from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer
from src.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="user")

    schedules = relationship("ScheduleModel", back_populates="owner", cascade="all, delete-orphan")

