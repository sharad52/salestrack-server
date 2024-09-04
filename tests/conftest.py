import pytest
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from salestrack.main import app
from salestrack.dbconfig.db_config import get_db
from salestrack.domain.models import Base
from salestrack.core.config import settings


TEST_DB_URL = settings.TEST_DB_URI

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

#Session Maker to manage session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Reflect models table str in db
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """New DB session with a rollback at end"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """test client which uses the override_db fixture to return a session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client: 
        yield test_client


@pytest.fixture()
def model_id() -> int:
    """Generate Random integer"""
    return random.randint(1, 10000)

