from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    DateTime,
    Date,
    Time,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime, date, time


class Base(DeclarativeBase):
    pass


metadata_obj = MetaData()


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    lessons: Mapped[list["Lessons"]] = relationship(back_populates="user")


class Lessons(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    teacher_name: Mapped[str]
    subject_name: Mapped[str]
    room: Mapped[str]

    startDate: Mapped[date] = mapped_column(Date, index=True)
    endDate: Mapped[date] = mapped_column(Date)

    startTime: Mapped[time] = mapped_column(Time)
    endTime: Mapped[time] = mapped_column(Time)

    repeat: Mapped[str]
    dayOfWeek: Mapped[str]

    user: Mapped["Users"] = relationship(back_populates="lessons")
    comments: Mapped[list["Comments"]] = relationship(back_populates="lesson")
    attendance: Mapped[list["Attendance"]] = relationship(back_populates="lesson")


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    lesson_date: Mapped[date] = mapped_column(Date)
    text: Mapped[str]

    lesson: Mapped["Lessons"] = relationship(back_populates="comments")


class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    lesson_date: Mapped[date] = mapped_column(Date)

    lesson: Mapped["Lessons"] = relationship(back_populates="attendance")
