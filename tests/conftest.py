import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.db.database import get_db
from app.models.message import Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_message():
    return {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system"
    }


@pytest.fixture
def invalid_message():
    return {
        "message_id": "msg-invalid",
        "session_id": "session-test",
        "content": "This message contains spam content",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }