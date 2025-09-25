import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.message import MessageCreate, Base
from app.services.message_service import MessageService
from app.core.errors import ValidationError, DuplicateError


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_service.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def message_service(db_session):
    return MessageService(db_session)


@pytest.fixture
def valid_message():
    return MessageCreate(
        message_id="test-msg-123",
        session_id="test-session-abc",
        content="This is a test message",
        timestamp=datetime(2023, 6, 15, 14, 30, 0),
        sender="user"
    )


def test_process_message_success(message_service, valid_message):
    """Test successful message processing"""
    result = message_service.process_message(valid_message)
    
    assert result.message_id == valid_message.message_id
    assert result.session_id == valid_message.session_id
    assert result.content == valid_message.content
    assert result.sender == valid_message.sender
    
    # Check metadata
    assert result.metadata.word_count == 5  # "This is a test message"
    assert result.metadata.character_count == len(valid_message.content)
    assert result.metadata.processed_at is not None


def test_process_message_with_inappropriate_content(message_service):
    """Test message processing with inappropriate content"""
    inappropriate_message = MessageCreate(
        message_id="test-msg-bad",
        session_id="test-session-bad",
        content="This message contains spam content",
        timestamp=datetime(2023, 6, 15, 14, 30, 0),
        sender="user"
    )
    
    with pytest.raises(ValidationError) as exc_info:
        message_service.process_message(inappropriate_message)
    
    assert "inappropriate content" in str(exc_info.value)


def test_process_duplicate_message(message_service, valid_message):
    """Test processing duplicate messages"""
    # First message should succeed
    message_service.process_message(valid_message)
    
    # Second message with same ID should fail
    with pytest.raises(DuplicateError):
        message_service.process_message(valid_message)


def test_get_messages_by_session(message_service):
    """Test retrieving messages by session"""
    # Create test messages
    messages = [
        MessageCreate(
            message_id="msg-1",
            session_id="session-1",
            content="First message",
            timestamp=datetime(2023, 6, 15, 14, 30, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="msg-2",
            session_id="session-1",
            content="Second message",
            timestamp=datetime(2023, 6, 15, 14, 31, 0),
            sender="system"
        )
    ]
    
    for message in messages:
        message_service.process_message(message)
    
    # Retrieve messages
    result = message_service.get_messages_by_session("session-1")
    
    assert len(result) == 2
    assert all(msg.session_id == "session-1" for msg in result)


def test_get_messages_with_sender_filter(message_service):
    """Test retrieving messages with sender filter"""
    # Create test messages
    messages = [
        MessageCreate(
            message_id="msg-user",
            session_id="session-filter",
            content="User message",
            timestamp=datetime(2023, 6, 15, 14, 30, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="msg-system",
            session_id="session-filter",
            content="System message",
            timestamp=datetime(2023, 6, 15, 14, 31, 0),
            sender="system"
        )
    ]
    
    for message in messages:
        message_service.process_message(message)
    
    # Get only user messages
    user_messages = message_service.get_messages_by_session("session-filter", sender="user")
    assert len(user_messages) == 1
    assert user_messages[0].sender == "user"
    
    # Get only system messages
    system_messages = message_service.get_messages_by_session("session-filter", sender="system")
    assert len(system_messages) == 1
    assert system_messages[0].sender == "system"


def test_get_messages_with_pagination(message_service):
    """Test message retrieval with pagination"""
    # Create multiple messages
    for i in range(5):
        message = MessageCreate(
            message_id=f"msg-{i}",
            session_id="session-page",
            content=f"Message {i}",
            timestamp=datetime(2023, 6, 15, 14, 30, i),
            sender="user"
        )
        message_service.process_message(message)
    
    # Test pagination
    page1 = message_service.get_messages_by_session("session-page", limit=2, offset=0)
    assert len(page1) == 2
    
    page2 = message_service.get_messages_by_session("session-page", limit=2, offset=2)
    assert len(page2) == 2
    
    page3 = message_service.get_messages_by_session("session-page", limit=2, offset=4)
    assert len(page3) == 1


def test_get_messages_invalid_sender(message_service):
    """Test retrieving messages with invalid sender"""
    with pytest.raises(ValidationError) as exc_info:
        message_service.get_messages_by_session("session-test", sender="invalid")
    
    assert "Sender must be 'user' or 'system'" in str(exc_info.value)


def test_content_filtering():
    """Test content filtering functionality"""
    from app.core.config import INAPPROPRIATE_WORDS
    
    # Ensure our test words are in the filter list
    assert "spam" in INAPPROPRIATE_WORDS
    assert "virus" in INAPPROPRIATE_WORDS


def test_word_count_calculation(message_service):
    """Test word count calculation"""
    message = MessageCreate(
        message_id="word-count-test",
        session_id="test-session",
        content="This is a test message with exactly eight words",
        timestamp=datetime(2023, 6, 15, 14, 30, 0),
        sender="user"
    )
    
    result = message_service.process_message(message)
    assert result.metadata.word_count == 9  # Corrected count


def test_character_count_calculation(message_service):
    """Test character count calculation"""
    content = "Hello, World!"
    message = MessageCreate(
        message_id="char-count-test",
        session_id="test-session",
        content=content,
        timestamp=datetime(2023, 6, 15, 14, 30, 0),
        sender="user"
    )
    
    result = message_service.process_message(message)
    assert result.metadata.character_count == len(content)