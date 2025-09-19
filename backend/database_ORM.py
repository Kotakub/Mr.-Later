from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from models import *
import inspect


def get_caller_name():
    return inspect.currentframe().f_back.f_back.f_code.co_name


# Асинхронные функции для работы с БД
async def get_user_by_email(db: AsyncSession, email: str):
    try:
        result = await db.execute(select(Users).where(Users.email == email))
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_user_by_login(db: AsyncSession, login: str):
    try:
        result = await db.execute(select(Users).where(Users.login == login))
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_lessons_by_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(Lessons).where(Lessons.user_id == user_id))
        return result.scalars().all()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_lessons_by_id(db: AsyncSession, lesson_id: int):
    try:
        result = await db.execute(select(Lessons).where(Lessons.id == lesson_id))
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def add_new_lesson(db: AsyncSession, lesson_data: dict):
    new_lesson = Lessons(**lesson_data)
    try:
        db.add(new_lesson)
        await db.commit()
        await db.refresh(new_lesson)
        return new_lesson

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def update_lesson(db: AsyncSession, lesson_data: dict):
    updated_lesson = lesson_data
    try:
        await db.execute(
            update(Lessons)
            .where(Lessons.id == updated_lesson.id)
            .values(**updated_lesson)
            .returning(Lessons)
        )
        await db.commit()
        return

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def delete_lesson_by_id(db: AsyncSession, lesson_id: int) -> bool:
    try:
        await db.execute(delete(Comments).where(Comments.lesson_id == lesson_id))
        await db.execute(delete(Attendance).where(Attendance.lesson_id == lesson_id))
        await db.execute(delete(Lessons).where(Lessons.id == lesson_id))
        await db.commit()

        return True

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_comments_by_lesson(db: AsyncSession, lesson_id: int):
    try:
        result = await db.execute(
            select(Comments).where(Comments.lesson_id == lesson_id)
        )
        return result.scalars().all()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_comments_by_lesson_and_date(
    db: AsyncSession, lesson_id: int, lesson_date
):
    try:
        result = await db.execute(
            select(Comments)
            .where(Comments.lesson_id == lesson_id)
            .where(Comments.lesson_date == lesson_date)
        )
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def add_new_comment(db: AsyncSession, comment_data: dict):
    new_comment = Comments(**comment_data)
    try:
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def update_comment(db: AsyncSession, comment_data: dict):
    updated_comment = comment_data
    try:
        await db.execute(
            update(Comments)
            .where(Comments.lesson_id == updated_comment["lesson_id"])
            .where(Comments.lesson_date == updated_comment["lesson_date"])
            .values(**updated_comment)
            .returning(Comments)
        )
        await db.commit()
        return

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def delete_comment(db: AsyncSession, lesson_id: int, lesson_date) -> bool:
    try:

        comment = get_comments_by_lesson_and_date(db, lesson_id, lesson_date)

        if not comment:
            return False

        await db.execute(
            delete(Comments)
            .where(Comments.lesson_id == lesson_id)
            .where(Comments.lesson_date == lesson_date)
        )
        await db.commit()

        return True

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def add_attendance_by_lesson_and_date(
    db: AsyncSession, lesson_id: int, lesson_date: date  # Убедитесь, что тип date
):
    try:
        new_attendance = Attendance(lesson_id=lesson_id, lesson_date=lesson_date)
        db.add(new_attendance)
        await db.commit()
        await db.refresh(new_attendance)
        return new_attendance

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_attendance_by_lesson_and_date(
    db: AsyncSession, lesson_id: int, lesson_date: date  # Убедитесь, что тип date
):
    try:
        result = await db.execute(
            select(Attendance)
            .where(Attendance.lesson_id == lesson_id)
            .where(Attendance.lesson_date == lesson_date)
        )
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e


async def get_attendance_by_lesson(db: AsyncSession, lesson_id: int):
    try:
        result = await db.execute(
            select(Attendance).where(Attendance.lesson_id == lesson_id)
        )
        return result.scalars().all()

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e
    return


async def delete_attendance_by_lesson_and_date(
    db: AsyncSession, lesson_id: int, lesson_date: date  # Убедитесь, что тип date
):
    try:
        attendance = await get_attendance_by_lesson_and_date(db, lesson_id, lesson_date)

        if not attendance:
            return False

        await db.execute(
            delete(Attendance)
            .where(Attendance.lesson_id == lesson_id)
            .where(Attendance.lesson_date == lesson_date)
        )
        await db.commit()
        return True

    except SQLAlchemyError as e:
        print(f"ОШИБКА В {get_caller_name()}")
        await db.rollback()
        raise e
