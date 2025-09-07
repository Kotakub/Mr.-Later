from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Импорты из вашей структуры проекта
from ..Database.database import get_async_session
from ..Database.models import Users
from ..config import settings
from ..Database.orm import *

# Создаем роутер
router = APIRouter(prefix="/auth", tags=["auth"])

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Настройка шифрования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Модель для данных токена
class TokenData:
    def __init__(self, username: Optional[str] = None):
        self.username = username


# Утилиты
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict, expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Зависимости с доступом к БД
async def get_current_user_db(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),  # Используем асинхронную зависимость
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# Роуты
@router.post("/register")
async def register(
    login: str,
    email: str,
    password: str,
    db: AsyncSession = Depends(get_async_session),  # Асинхронная сессия
):
    # Проверка существования пользователя
    if await get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    if await get_user_by_login(db, login):
        raise HTTPException(status_code=400, detail="Логин уже занят")

    # Создание пользователя
    hashed_password = get_password_hash(password)
    user = Users(login=login, email=email, password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Создание токена
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "login": user.login, "email": user.email},
    }


@router.post("/login")
async def login(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_async_session),  # Асинхронная сессия
):
    # Поиск пользователя по email или логину
    user = await get_user_by_email(db, username)
    if not user:
        user = await get_user_by_login(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный email/логин")

    # Проверка пароля
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # Создание токена
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "login": user.login, "email": user.email},
    }
