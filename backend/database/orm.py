from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Импорты из вашей структуры проекта
from database import get_async_session
from models import Users
from ..config import settings


# Асинхронные функции для работы с БД
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[Users]:
    result = await db.execute(select(Users).where(Users.email == email))
    return result.scalar_one_or_none()


async def get_user_by_login(db: AsyncSession, login: str) -> Optional[Users]:
    result = await db.execute(select(Users).where(Users.login == login))
    return result.scalar_one_or_none()
