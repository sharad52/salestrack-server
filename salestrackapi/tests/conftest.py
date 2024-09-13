import pytest
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from salestrackapi.main import app
from salestrackapi.dbconfig.db_config import get_db, Base
from salestrackapi.config import settings


TEST_DB_URL = settings.TEST_DB_URI

engine = create_engine(TEST_DB_URL)

#Session Maker to manage session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Reflect models table str in db
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    try:
        """New DB session with a rollback at end"""
        connection = engine.connect()
        print("Connection succesful!!!.")
        transaction = connection.begin()
        session = TestingSessionLocal(bind=connection)
        yield session
        session.close()
        transaction.rollback()
        connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")

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
def item_id() -> int:
    """Generate Random integer"""
    return random.randint(1, 10000)


@pytest.fixture()
def family_payload(item_id):
    """Sample payload for family"""
    return {
        "id": item_id,
        "name": "Book"
    }


@pytest.fixture()
def product_payload(item_id, family_payload):
    """Sample payload for product"""
    return {
        "id": item_id,
        "name": "Atomic Habbits",
        "family_id": family_payload['id'],
        "price": 1350
    }


@pytest.fixture()
def product_payload_updated(item_id, family_payload):
    """Sample payload for updated Product"""
    return {
        "id": item_id,
        "name": "Ikigai",
        "family_id": family_payload["id"],
        "price": 1200
    }


@pytest.fixture()
def excel_load_data_payload():
    """Mock Excel Data"""
    data = {
        'Family': ['Electronics', 'Books'],
        'Product Name': ['Laptop', 'Fluent Python'],
        'Product ID': [101, 102],
        'Price': [999.99, 29.99],
        '2024-01-01': [10, 5],
        '2024-02-01': [15, 10]
    }
    return data
