from database import session, engine
from models import metadata_obj

metadata_obj.create_all(engine)
