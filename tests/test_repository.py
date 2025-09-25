import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.message import MessageCreate, Base
from app.repository.message_repository import MessageRepository
from app.core.errors import DuplicateError


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_repository.db"

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
def message_repository(db_session):
    return MessageRepository(db_session)


@pytest.fixture
def sample_message_data():
    return MessageCreate(
        message_id="repo-test-123",
        session_id="repo-session-abc",
        content="Repository test message",
        timestamp=datetime(2023, 6, 15, 14, 30, 0),
        sender="user"
    )


def test_create_message(message_repository, sample_message_data):
    """Test creating a message in the repository"""
    word_count = 3
    character_count = len(sample_message_data.content)
    processed_at = datetime.now(timezone.utc)
    
    result = message_repository.create_message(
        sample_message_data, 
        word_count, 
        character_count, 
        processed_at
    )
    
    assert result.message_id == sample_message_data.message_id
    assert result.session_id == sample_message_data.session_id
    assert result.content == sample_message_data.content
    assert result.sender == sample_message_data.sender.value
    assert result.word_count == word_count
    assert result.character_count == character_count
    # Database stores datetime as naive, so compare without timezone info
    assert result.processed_at.replace(tzinfo=timezone.utc) == processed_at


def test_create_duplicate_message(message_repository, sample_message_data):
    """Test creating a message with duplicate ID"""
    word_count = 3
    character_count = len(sample_message_data.content)
    processed_at = datetime.now(timezone.utc)
    
    # First creation should succeed
    message_repository.create_message(
        sample_message_data, 
        word_count, 
        character_count, 
        processed_at
    )
    
    # Second creation with same ID should fail
    with pytest.raises(DuplicateError):
        message_repository.create_message(
            sample_message_data, 
            word_count, 
            character_count, 
            processed_at
        )


def test_get_messages_by_session(message_repository):
    """Test retrieving messages by session ID"""
    # Create test messages
    messages_data = [
        MessageCreate(
            message_id="session-msg-1",
            session_id="test-session",
            content="First message",
            timestamp=datetime(2023, 6, 15, 14, 30, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="session-msg-2",
            session_id="test-session",
            content="Second message",
            timestamp=datetime(2023, 6, 15, 14, 31, 0),
            sender="system"
        ),
        MessageCreate(
            message_id="other-session-msg",
            session_id="other-session",
            content="Other session message",
            timestamp=datetime(2023, 6, 15, 14, 32, 0),
            sender="user"
        )
    ]
    
    # Store messages
    for msg_data in messages_data:
        message_repository.create_message(
            msg_data, 
            len(msg_data.content.split()), 
            len(msg_data.content), 
            datetime.now(timezone.utc)
        )
    
    # Retrieve messages for specific session
    session_messages = message_repository.get_messages_by_session("test-session")
    
    assert len(session_messages) == 2
    assert all(msg.session_id == "test-session" for msg in session_messages)


def test_get_messages_with_sender_filter(message_repository):
    """Test retrieving messages with sender filter"""
    # Create messages with different senders
    messages_data = [
        MessageCreate(
            message_id="user-msg-1",
            session_id="filter-session",
            content="User message 1",
            timestamp=datetime(2023, 6, 15, 14, 30, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="system-msg-1",
            session_id="filter-session",
            content="System message 1",
            timestamp=datetime(2023, 6, 15, 14, 31, 0),
            sender="system"
        ),
        MessageCreate(
            message_id="user-msg-2",
            session_id="filter-session",
            content="User message 2",
            timestamp=datetime(2023, 6, 15, 14, 32, 0),
            sender="user"
        )
    ]
    
    # Store messages
    for msg_data in messages_data:
        message_repository.create_message(
            msg_data, 
            len(msg_data.content.split()), 
            len(msg_data.content), 
            datetime.now(timezone.utc)
        )
    
    # Get only user messages
    user_messages = message_repository.get_messages_by_session("filter-session", sender="user")
    assert len(user_messages) == 2
    assert all(msg.sender == "user" for msg in user_messages)
    
    # Get only system messages
    system_messages = message_repository.get_messages_by_session("filter-session", sender="system")
    assert len(system_messages) == 1
    assert system_messages[0].sender == "system"


def test_get_messages_with_pagination(message_repository):
    """Test message retrieval with pagination"""
    # Create multiple messages
    messages_data = []
    for i in range(5):
        messages_data.append(MessageCreate(
            message_id=f"page-msg-{i}",
            session_id="page-session",
            content=f"Message {i}",
            timestamp=datetime(2023, 6, 15, 14, 30, i),
            sender="user"
        ))
    
    # Store messages
    for msg_data in messages_data:
        message_repository.create_message(
            msg_data, 
            len(msg_data.content.split()), 
            len(msg_data.content), 
            datetime.now(timezone.utc)
        )
    
    # Test pagination
    page1 = message_repository.get_messages_by_session("page-session", limit=2, offset=0)
    assert len(page1) == 2
    
    page2 = message_repository.get_messages_by_session("page-session", limit=2, offset=2)
    assert len(page2) == 2
    
    page3 = message_repository.get_messages_by_session("page-session", limit=2, offset=4)
    assert len(page3) == 1


def test_get_message_by_id(message_repository, sample_message_data):
    """Test retrieving a message by ID"""
    word_count = 3
    character_count = len(sample_message_data.content)
    processed_at = datetime.now(timezone.utc)
    
    # Create message
    created_message = message_repository.create_message(
        sample_message_data, 
        word_count, 
        character_count, 
        processed_at
    )
    
    # Retrieve by ID
    retrieved_message = message_repository.get_message_by_id(sample_message_data.message_id)
    
    assert retrieved_message is not None
    assert retrieved_message.message_id == sample_message_data.message_id
    assert retrieved_message.id == created_message.id


def test_get_nonexistent_message_by_id(message_repository):
    """Test retrieving a non-existent message by ID"""
    result = message_repository.get_message_by_id("non-existent-id")
    assert result is None


def test_message_exists(message_repository, sample_message_data):
    """Test checking if a message exists"""
    # Initially should not exist
    assert not message_repository.message_exists(sample_message_data.message_id)
    
    # Create message
    message_repository.create_message(
        sample_message_data, 
        3, 
        len(sample_message_data.content), 
        datetime.now(timezone.utc)
    )
    
    # Now should exist
    assert message_repository.message_exists(sample_message_data.message_id)


def test_empty_session_query(message_repository):
    """Test querying messages for a session with no messages"""
    messages = message_repository.get_messages_by_session("empty-session")
    assert len(messages) == 0


def test_message_ordering(message_repository):
    """Test that messages are returned in correct order (newest first)"""
    # Create messages with different timestamps
    messages_data = [
        MessageCreate(
            message_id="old-msg",
            session_id="order-session",
            content="Old message",
            timestamp=datetime(2023, 6, 15, 14, 30, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="new-msg",
            session_id="order-session",
            content="New message",
            timestamp=datetime(2023, 6, 15, 14, 35, 0),
            sender="user"
        ),
        MessageCreate(
            message_id="middle-msg",
            session_id="order-session",
            content="Middle message",
            timestamp=datetime(2023, 6, 15, 14, 32, 0),
            sender="user"
        )
    ]
    
    # Store messages
    for msg_data in messages_data:
        message_repository.create_message(
            msg_data, 
            len(msg_data.content.split()), 
            len(msg_data.content), 
            datetime.now(timezone.utc)
        )
    
    # Retrieve messages
    messages = message_repository.get_messages_by_session("order-session")
    
    # Should be ordered by timestamp descending (newest first)
    assert len(messages) == 3
    assert messages[0].message_id == "new-msg"
    assert messages[1].message_id == "middle-msg"
    assert messages[2].message_id == "old-msg"