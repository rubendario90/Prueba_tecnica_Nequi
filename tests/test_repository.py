import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.message import Base, MessageCreate
from app.repository.message_repository import MessageRepository
from app.core.errors import DuplicateError

# Utiliza una base en memoria para pruebas
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_message_success(db_session):
    repo = MessageRepository(db_session)
    msg_data = MessageCreate(
        message_id="msg-1",
        session_id="sess-1",
        content="Hola mundo",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    result = repo.create_message(msg_data, word_count=2, character_count=10, processed_at="2025-09-25T10:00:01Z")
    assert result.message_id == "msg-1"
    assert result.word_count == 2
    assert result.character_count == 10

def test_create_message_duplicate(db_session):
    repo = MessageRepository(db_session)
    msg_data = MessageCreate(
        message_id="msg-dup",
        session_id="sess-1",
        content="Hola mundo",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    repo.create_message(msg_data, 2, 10, "2025-09-25T10:00:01Z")
    with pytest.raises(DuplicateError):
        repo.create_message(msg_data, 2, 10, "2025-09-25T10:00:02Z")

def test_get_messages_by_session(db_session):
    repo = MessageRepository(db_session)
    data1 = MessageCreate(
        message_id="msg-2",
        session_id="sess-2",
        content="Uno",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    data2 = MessageCreate(
        message_id="msg-3",
        session_id="sess-2",
        content="Dos",
        timestamp="2025-09-25T10:01:00Z",
        sender="system"
    )
    repo.create_message(data1, 1, 3, "2025-09-25T10:00:01Z")
    repo.create_message(data2, 1, 3, "2025-09-25T10:01:01Z")
    msgs = repo.get_messages_by_session("sess-2")
    assert len(msgs) == 2
    msgs_user = repo.get_messages_by_session("sess-2", sender="user")
    assert len(msgs_user) == 1
    assert msgs_user[0].sender == "user"

def test_get_message_by_id(db_session):
    repo = MessageRepository(db_session)
    data = MessageCreate(
        message_id="msg-4",
        session_id="sess-3",
        content="Test",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    repo.create_message(data, 1, 4, "2025-09-25T10:00:01Z")
    msg = repo.get_message_by_id("msg-4")
    assert msg is not None
    assert msg.message_id == "msg-4"
    assert repo.get_message_by_id("non-existent") is None

def test_message_exists(db_session):
    repo = MessageRepository(db_session)
    data = MessageCreate(
        message_id="msg-5",
        session_id="sess-4",
        content="Exists",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    repo.create_message(data, 1, 6, "2025-09-25T10:00:01Z")
    assert repo.message_exists("msg-5") is True
    assert repo.message_exists("not-exists") is False