import asyncio
from sqlalchemy import text
from database_main import engine, session
from config import settings


async def add_room_column():
    async with engine.begin() as conn:
        # Проверяем, существует ли уже столбец room
        result = await conn.execute(text("PRAGMA table_info(lessons)"))
        columns = [row[1] for row in result]

        if "room" not in columns:
            # Добавляем новый столбец
            await conn.execute(text("ALTER TABLE lessons ADD COLUMN room TEXT"))
            print("Столбец 'room' успешно добавлен в таблицу 'lessons'")
        else:
            print("Столбец 'room' уже существует в таблице 'lessons'")


async def main():
    await add_room_column()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
