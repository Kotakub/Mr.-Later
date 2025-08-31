from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from config import settings

engine = create_engine(url=settings.DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass
