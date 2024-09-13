# import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from salestrackapifjf.core.config import settings


engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




        