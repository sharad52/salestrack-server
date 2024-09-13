from structlog import get_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from salestrack_utils.core.settings import CoreSettings


logger = get_logger(__name__)

Base = declarative_base()

class DatabaseManger:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Database initialization and create tables."""
        logger.info("DB connection initialized.")
        Base.metadata.create_all(bind=self.engine)
    
    def connect(self):
        yield self.sessionlocal()

    def disconnect(self):
        """Close the database connection"""
        self.sessionlocal().close()
        self.engine.dispose()
        logger.info("Db disconnected...")

    
def init_database(settings: CoreSettings) -> DatabaseManger:
    db=DatabaseManger(f"{settings.pg_dsn}")
    return db
