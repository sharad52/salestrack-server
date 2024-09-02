from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from salestrack.core.config import settings

DB_URI = 'postgresql://username:password@hostname/dbname'

engine = create_engine(settings.DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


        