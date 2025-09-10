from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from models import *


# Асинхронные функции для работы с БД
async def get_user_by_email(db: AsyncSession, email: str):
    try:
        result = await db.execute(select(Users).where(Users.email == email))
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_user_by_login(db: AsyncSession, login: str):
    try:
        result = await db.execute(select(Users).where(Users.login == login))
        return result.scalar_one_or_none()

    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_lessons_by_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(Lessons).where(Lessons.user_id == user_id))
        return result.scalars().all()

    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def get_comments_by_lesson(db: AsyncSession, lesson_id: int):
    try:
        result = await db.execute(
            select(Comments).where(Comments.lesson_id == lesson_id)
        )
        return result.scalars().all()

    except SQLAlchemyError as e:
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
        await db.rollback()
        raise e


async def get_comments_by_lesson(db: AsyncSession, lesson_id: int):
    try:
        result = await db.execute(
            select(Comments).where(Comments.lesson_id == lesson_id)
        )
        return result.scalars().all()

    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    return


async def delete_lesson_by_id(db: AsyncSession, lesson_id: int) -> bool:
    try:

        result = await db.execute(select(Lessons).where(Lessons.id == lesson_id))
        lesson = result.scalar_one_or_none()

        if not lesson:
            return False

        await db.execute(delete(Lessons).where(Lessons.id == lesson_id))
        await db.commit()

        return True

    except SQLAlchemyError as e:
        await db.rollback()
        raise e
