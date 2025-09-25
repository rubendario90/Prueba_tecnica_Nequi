import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.message import Base, MessageCreate
from app.repository.message_repository import MessageRepository
from app.core.errors import DuplicateError
from datetime import datetime
from zoneinfo import ZoneInfo

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
        timestamp=datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="user"
    )
    result = repo.create_message(
        msg_data,
        word_count=2,
        character_count=10,
        processed_at=datetime(2025, 9, 25, 10, 0, 1, tzinfo=ZoneInfo("America/Bogota"))
    )
    assert result.message_id == "msg-1"
    assert result.word_count == 2
    assert result.character_count == 10

def test_create_message_duplicate(db_session):
    repo = MessageRepository(db_session)
    msg_data = MessageCreate(
        message_id="msg-dup",
        session_id="sess-1",
        content="Hola mundo",
        timestamp=datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="user"
    )
    repo.create_message(msg_data, 2, 10, datetime(2025, 9, 25, 10, 0, 1, tzinfo=ZoneInfo("America/Bogota")))
    with pytest.raises(DuplicateError):
        repo.create_message(msg_data, 2, 10, datetime(2025, 9, 25, 10, 0, 2, tzinfo=ZoneInfo("America/Bogota")))

def test_get_messages_by_session(db_session):
    repo = MessageRepository(db_session)
    data1 = MessageCreate(
        message_id="msg-2",
        session_id="sess-2",
        content="Uno",
        timestamp=datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="user"
    )
    data2 = MessageCreate(
        message_id="msg-3",
        session_id="sess-2",
        content="Dos",
        timestamp=datetime(2025, 9, 25, 10, 1, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="system"
    )
    repo.create_message(data1, 1, 3, datetime(2025, 9, 25, 10, 0, 1, tzinfo=ZoneInfo("America/Bogota")))
    repo.create_message(data2, 1, 3, datetime(2025, 9, 25, 10, 1, 1, tzinfo=ZoneInfo("America/Bogota")))
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
        timestamp=datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="user"
    )
    repo.create_message(data, 1, 4, datetime(2025, 9, 25, 10, 0, 1, tzinfo=ZoneInfo("America/Bogota")))
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
        timestamp=datetime(2025, 9, 25, 10, 0, 0, tzinfo=ZoneInfo("America/Bogota")),
        sender="user"
    )
    repo.create_message(data, 1, 6, datetime(2025, 9, 25, 10, 0, 1, tzinfo=ZoneInfo("America/Bogota")))
    assert repo.message_exists("msg-5") is True
    assert repo.message_exists("not-exists") is False