from sqlalchemy import text, insert
from database import engine
from models import metadata_obj


async def create_tables():
    engine.echo = False
    metadata_obj.create_all(engine)
    engine.echo = True
