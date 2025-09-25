import pytest
from fastapi.testclient import TestClient


def test_create_message_success(client: TestClient, sample_message):
    """Test successful message creation"""
    response = client.post("/api/messages", json=sample_message)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert data["data"]["message_id"] == sample_message["message_id"]
    assert data["data"]["session_id"] == sample_message["session_id"]
    assert data["data"]["content"] == sample_message["content"]
    assert data["data"]["sender"] == sample_message["sender"]
    assert "metadata" in data["data"]
    assert "word_count" in data["data"]["metadata"]
    assert "character_count" in data["data"]["metadata"]
    assert "processed_at" in data["data"]["metadata"]


def test_create_message_with_inappropriate_content(client: TestClient, invalid_message):
    """Test message creation with inappropriate content"""
    response = client.post("/api/messages", json=invalid_message)
    
    assert response.status_code == 400
    data = response.json()
    
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "INVALID_FORMAT"
    assert "inappropriate" in data["detail"]["error"]["message"].lower()


def test_create_message_duplicate_id(client: TestClient, sample_message):
    """Test creating message with duplicate ID"""
    # First message should succeed
    response = client.post("/api/messages", json=sample_message)
    assert response.status_code == 200
    
    # Second message with same ID should fail
    response = client.post("/api/messages", json=sample_message)
    assert response.status_code == 409
    data = response.json()
    
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "DUPLICATE_RESOURCE"


def test_create_message_invalid_sender(client: TestClient, sample_message):
    """Test message creation with invalid sender"""
    invalid_sender_message = sample_message.copy()
    invalid_sender_message["sender"] = "invalid_sender"
    
    response = client.post("/api/messages", json=invalid_sender_message)
    assert response.status_code == 422  # Pydantic validation error


def test_create_message_empty_content(client: TestClient, sample_message):
    """Test message creation with empty content"""
    empty_content_message = sample_message.copy()
    empty_content_message["content"] = ""
    
    response = client.post("/api/messages", json=empty_content_message)
    assert response.status_code == 422  # Pydantic validation error


def test_get_messages_by_session(client: TestClient):
    """Test retrieving messages by session ID"""
    # Create some test messages
    messages = [
        {
            "message_id": "msg-1",
            "session_id": "session-test",
            "content": "Hello from user",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user"
        },
        {
            "message_id": "msg-2",
            "session_id": "session-test",
            "content": "Hello from system",
            "timestamp": "2023-06-15T14:31:00Z",
            "sender": "system"
        }
    ]
    
    for message in messages:
        response = client.post("/api/messages", json=message)
        assert response.status_code == 200
    
    # Get messages for session
    response = client.get("/api/messages/session-test")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 2
    assert "pagination" in data


def test_get_messages_with_sender_filter(client: TestClient):
    """Test retrieving messages with sender filter"""
    # Create test messages
    messages = [
        {
            "message_id": "msg-3",
            "session_id": "session-filter",
            "content": "User message",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user"
        },
        {
            "message_id": "msg-4",
            "session_id": "session-filter",
            "content": "System message",
            "timestamp": "2023-06-15T14:31:00Z",
            "sender": "system"
        }
    ]
    
    for message in messages:
        response = client.post("/api/messages", json=message)
        assert response.status_code == 200
    
    # Get only user messages
    response = client.get("/api/messages/session-filter?sender=user")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["sender"] == "user"


def test_get_messages_with_pagination(client: TestClient):
    """Test message retrieval with pagination"""
    # Create multiple messages
    for i in range(5):
        message = {
            "message_id": f"msg-page-{i}",
            "session_id": "session-page",
            "content": f"Message {i}",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user"
        }
        response = client.post("/api/messages", json=message)
        assert response.status_code == 200
    
    # Test pagination
    response = client.get("/api/messages/session-page?limit=2&offset=0")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 2
    assert data["pagination"]["limit"] == 2
    assert data["pagination"]["offset"] == 0


def test_get_messages_empty_session(client: TestClient):
    """Test retrieving messages for non-existent session"""
    response = client.get("/api/messages/non-existent-session")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) == 0


def test_get_messages_invalid_sender_filter(client: TestClient):
    """Test retrieving messages with invalid sender filter"""
    response = client.get("/api/messages/session-test?sender=invalid")
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "INVALID_FORMAT"


def test_root_endpoint(client: TestClient):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "mensaje" in data
    assert "version" in data