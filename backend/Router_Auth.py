from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


from database_main import get_async_session
from models import Users
from config import settings
from database_ORM import *

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData:
    def __init__(self, username: Optional[str] = None):
        self.username = username


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


async def get_current_user_db(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),
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
        print("PAYLOAD", payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# Роутеры
@router.post("/register")
async def register(request: Request, db: AsyncSession = Depends(get_async_session)):
    try:

        # Получаем JSON из тела запроса
        json_data = await request.json()

        # Валидация обязательных полей
        required_fields = ["login", "email", "password"]
        for field in required_fields:
            if field not in json_data:
                error_msg = f"Отсутствует обязательное поле: {field}"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg,
                )

        # Проверка уникальности email
        existing_user_email = await get_user_by_email(db, json_data["email"])

        if existing_user_email is not None:
            error_msg = "Email уже зарегистрирован"
            raise HTTPException(status_code=400, detail=error_msg)

        # Проверка уникальности логина
        existing_user_login = await get_user_by_login(db, json_data["login"])

        if existing_user_login is not None:
            error_msg = "Логин уже занят"
            raise HTTPException(status_code=400, detail=error_msg)

        # Добавление пользователя
        hashed_password = get_password_hash(json_data["password"])

        user = Users(
            login=json_data["login"], email=json_data["email"], password=hashed_password
        )
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

    except HTTPException as he:
        print("ОШИБКА РЕГИСТР")
        await db.rollback()
        raise he
    except Exception as e:
        import traceback

        print("ОШИБКА РЕГИСТР")
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка регистрации: {str(e)}",
        )


@router.post("/login")
async def login(request: Request, db: AsyncSession = Depends(get_async_session)):
    try:
        # Получаем JSON из тела запроса
        json_data = await request.json()

        # Валидация обязательных полей
        required_fields = ["username", "password"]
        for field in required_fields:
            if field not in json_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Отсутствует обязательное поле: {field}",
                )

        username = json_data["username"]
        password = json_data["password"]

        # Поиск пользователя
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

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка входа: {str(e)}",
        )
