# import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from salestrack.core.config import settings


engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




        