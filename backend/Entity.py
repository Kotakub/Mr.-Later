from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, Numeric, SmallInteger, String, Table, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    login: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    fullName: Mapped[str] = mapped_column(String)
    user_id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, primary_key=True)

    schedule: Mapped[List['Schedule']] = relationship('Schedule', back_populates='author')
    schedule_: Mapped[List['Schedule']] = relationship('Schedule', secondary='follow', back_populates='user')


class Schedule(Base):
    __tablename__ = 'schedule'

    author_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    name: Mapped[str] = mapped_column(String)
    isPublic: Mapped[bool] = mapped_column(Boolean)
    schedule_id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric, primary_key=True)

    author: Mapped['User'] = relationship('User', back_populates='schedule')
    user: Mapped[List['User']] = relationship('User', secondary='follow', back_populates='schedule_')
    lesson: Mapped[List['Lesson']] = relationship('Lesson', back_populates='schedule')


t_follow = Table(
    'follow', Base.metadata,
    Column('user_id', ForeignKey('user.user_id'), primary_key=True, nullable=False),
    Column('schedule_id', ForeignKey('schedule.schedule_id'), primary_key=True, nullable=False)
)


class Lesson(Base):
    __tablename__ = 'lesson'

    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule.schedule_id'))
    subject_name: Mapped[str] = mapped_column(String)
    startDate: Mapped[datetime.date] = mapped_column(Date)
    endDate: Mapped[datetime.date] = mapped_column(Date)
    startTime: Mapped[datetime.time] = mapped_column(Time)
    endTime: Mapped[datetime.time] = mapped_column(Time)
    repeat: Mapped[int] = mapped_column(SmallInteger)
    dayOfWeek: Mapped[int] = mapped_column(SmallInteger)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    teacher_name: Mapped[Optional[str]] = mapped_column(String)

    schedule: Mapped['Schedule'] = relationship('Schedule', back_populates='lesson')
    attendance: Mapped[List['Attendance']] = relationship('Attendance', back_populates='lesson')
    blur: Mapped[List['Blur']] = relationship('Blur', back_populates='lesson')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='lesson')


class Attendance(Base):
    __tablename__ = 'attendance'

    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson.id', ondelete='CASCADE'), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)

    lesson: Mapped['Lesson'] = relationship('Lesson', back_populates='attendance')


class Blur(Base):
    __tablename__ = 'blur'

    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson.id', ondelete='CASCADE'), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)

    lesson: Mapped['Lesson'] = relationship('Lesson', back_populates='blur')


class Comment(Base):
    __tablename__ = 'comment'

    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson.id', ondelete='CASCADE'), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    text: Mapped[Optional[str]] = mapped_column(String)

    lesson: Mapped['Lesson'] = relationship('Lesson', back_populates='comment')
