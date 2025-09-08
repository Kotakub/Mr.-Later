from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Users


# Асинхронные функции для работы с БД
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[Users]:
    result = await db.execute(select(Users).where(Users.email == email))
    return result.scalar_one_or_none()


async def get_user_by_login(db: AsyncSession, login: str) -> Optional[Users]:
    result = await db.execute(select(Users).where(Users.login == login))
    return result.scalar_one_or_none()
