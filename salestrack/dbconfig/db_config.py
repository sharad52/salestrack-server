import databases
from sqlalchemy import create_engine, MetaData
from salestrack.core.config import settings


database = databases.Database(settings.DATABASE_URI)
metadata = MetaData()

engine = create_engine(settings.DATABASE_URI)
metadata.create_all(engine)



        