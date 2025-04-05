from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, Float, JSON, ForeignKey
from src.infrastructure.database import Base


class ScheduleModel(Base):
    __tablename__ = 'schedules'

    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)

    owner = relationship("UserModel", back_populates="schedules")
    statistics = relationship("ScheduleStatisticsModel", back_populates="schedule", uselist=False)
    votes = relationship("ScheduleVoteModel", back_populates="schedule")


class ScheduleStatisticsModel(Base):
    __tablename__ = 'schedule_statistics'

    id: Mapped[int] = mapped_column(primary_key=True)
    statistics_id: Mapped[int] = mapped_column(
        ForeignKey('schedules.schedule_id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )
    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    schedule = relationship("ScheduleModel", back_populates="statistics")


class ScheduleVoteModel(Base):
    __tablename__ = 'schedule_votes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedules.schedule_id', ondelete='CASCADE'), nullable=False)
    vote_type: Mapped[str] = mapped_column(String, nullable=False)

    schedule = relationship("ScheduleModel", back_populates="votes")
