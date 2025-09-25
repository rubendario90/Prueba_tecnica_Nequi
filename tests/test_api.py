import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import app

import pytest
from fastapi.testclient import TestClient
from app.db.database import SessionLocal
from app.models.message import Message

# Fixture para limpiar  
@pytest.fixture(autouse=True)
def clean_messages():
    db = SessionLocal()
    db.query(Message).delete()
    db.commit()
    db.close()

client = TestClient(app)

def test_create_message_success():
    data = {
        "message_id": "msg-test-1",
        "session_id": "session-1",
        "content": "Hola mundo",
        "timestamp": "2025-09-25T10:00:00Z",
        "sender": "user"
    }
    response = client.post("/api/messages", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_message_invalid_sender():
    data = {
        "message_id": "msg-test-2",
        "session_id": "session-1",
        "content": "Hola mundo",
        "timestamp": "2025-09-25T10:00:00Z",
        "sender": "otro"
    }
    response = client.post("/api/messages", json=data)
    assert response.status_code == 422