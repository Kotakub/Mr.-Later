from database_main import create_tables
import asyncio
from sqlalchemy import inspect
from database_main import engine


from sqlalchemy import text


async def get_tables_info_sqlite():
    async with engine.connect() as conn:
        # Для SQLite используем другой запрос
        result = await conn.execute(
            text(
                """
            SELECT name, type 
            FROM sqlite_master 
            WHERE type IN ('table', 'view')
            ORDER BY name
        """
            )
        )
        tables = result.fetchall()

        print("Таблицы в базе данных SQLite:")
        for table in tables:
            print(f"- {table[0]} ({table[1]})")


if __name__ == "__main__":
    asyncio.run(get_tables_info_sqlite())
