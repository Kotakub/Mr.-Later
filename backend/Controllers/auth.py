from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Импорты из вашей структуры проекта
from database.database import get_db
from database.models import Users
from config import settings  # Импортируем настройки из config.py

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


# Функция для создания JWT токена (использует настройки из config)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Dependency для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return {"username": token_data.username}


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


def get_user_by_email(db: Session, email: str) -> Users:
    return db.query(Users).filter(Users.email == email).first()


def get_user_by_login(db: Session, login: str) -> Users:
    return db.query(Users).filter(Users.login == login).first()


# Зависимости с доступом к БД
async def get_current_user_db(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
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

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# Роуты
@router.post("/register")
async def register(
    login: str, email: str, password: str, db: Session = Depends(get_db)
):
    # Проверка существования пользователя
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    if get_user_by_login(db, login):
        raise HTTPException(status_code=400, detail="Логин уже занят")

    # Создание пользователя
    hashed_password = get_password_hash(password)

    user = Users(login=login, email=email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Создание токена
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "login": user.login, "email": user.email},
    }


@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    # Поиск пользователя по email или логину
    user = get_user_by_email(db, username)
    if not user:
        user = get_user_by_login(db, username)
        if not user:
            raise HTTPException(
                status_code=401, detail="Неверный email/логин или пароль"
            )

    # Проверка пароля
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email/логин или пароль")

    # Создание токена
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "login": user.login, "email": user.email},
    }


@router.get("/me")
async def get_me(current_user: Users = Depends(get_current_user_db)):
    return {
        "id": current_user.id,
        "login": current_user.login,
        "email": current_user.email,
    }


@router.post("/logout")
async def logout():
    return {"message": "Успешный выход из системы"}


@router.get("/check-auth")
async def check_auth(current_user: Users = Depends(get_current_user_db)):
    return {"authenticated": True, "user": current_user.login}


@router.put("/me/update-password")
async def update_password(
    old_password: str,
    new_password: str,
    current_user: Users = Depends(get_current_user_db),
    db: Session = Depends(get_db),
):
    """Обновление пароля пользователя"""
    if not verify_password(old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Текущий пароль неверен")

    current_user.password = get_password_hash(new_password)
    db.commit()

    return {"message": "Пароль успешно обновлен"}


@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db), current_user: Users = Depends(get_current_user_db)
):
    """Получение всех пользователей (только для аутентифицированных)"""
    users = db.query(Users).all()
    return [{"id": user.id, "login": user.login, "email": user.email} for user in users]


# Экспортируем зависимости для использования в других модулях
__all__ = [
    "get_current_user",
    "get_current_user_db",
    "oauth2_scheme",
    "create_access_token",
]
