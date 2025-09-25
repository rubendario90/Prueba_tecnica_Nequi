import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.message import Base, MessageCreate
from app.services.message_service import MessageService
from app.core.errors import DuplicateError, NotFoundError

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_process_message_success(db_session):
    service = MessageService(db_session)
    data = MessageCreate(
        message_id="msg-10",
        session_id="sess-service",
        content="Hola mundo prueba",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    result = service.process_message(data)
    assert result.message_id == "msg-10"
    assert result.metadata.word_count == 3
    assert result.metadata.character_count == len("Hola mundo prueba")

def test_process_message_duplicate(db_session):
    service = MessageService(db_session)
    data = MessageCreate(
        message_id="msg-dup-service",
        session_id="sess-service",
        content="Hola mundo",
        timestamp="2025-09-25T10:00:00Z",
        sender="user"
    )
    service.process_message(data)
    with pytest.raises(DuplicateError):
        service.process_message(data)

def test_get_messages_by_session(db_session):
    service = MessageService(db_session)
    data1 = MessageCreate(
        message_id="msg-20",
        session_id="sess-get",
        content="Uno",
        timestamp="2025-09-25T10:10:00Z",
        sender="user"
    )
    data2 = MessageCreate(
        message_id="msg-21",
        session_id="sess-get",
        content="Dos",
        timestamp="2025-09-25T10:11:00Z",
        sender="system"
    )
    service.process_message(data1)
    service.process_message(data2)
    messages = service.get_messages_by_session(session_id="sess-get")
    assert len(messages) == 2
    only_user = service.get_messages_by_session(session_id="sess-get", sender="user")
    assert len(only_user) == 1
    assert only_user[0].sender == "user"

def test_get_messages_by_session_empty(db_session):
    service = MessageService(db_session)
    messages = service.get_messages_by_session(session_id="empty-session")
    assert messages == []