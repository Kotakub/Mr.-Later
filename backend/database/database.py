from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from ..configs import settings
from models import metadata_obj

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with session() as sess:
        yield sess


async def create_tables():
    metadata_obj.create_all(engine)


class Base(DeclarativeBase):
    pass
