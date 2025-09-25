#!/usr/bin/env python3
"""
Example usage of the Message Processing API

This script demonstrates how to interact with the API endpoints.
Make sure the server is running on http://localhost:8000 before executing.

Usage:
    python example_usage.py

Requirements:
    pip install requests
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def create_message(message_data):
    """Create a new message via the API"""
    url = f"{BASE_URL}/api/messages"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=message_data, headers=headers)
    print(f"POST /api/messages - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response

def get_messages(session_id, sender=None, limit=10, offset=0):
    """Get messages for a session"""
    url = f"{BASE_URL}/api/messages/{session_id}"
    params = {"limit": limit, "offset": offset}
    if sender:
        params["sender"] = sender
    
    response = requests.get(url, params=params)
    print(f"GET /api/messages/{session_id} - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response

def main():
    """Demonstrate API usage"""
    print("=" * 50)
    print("Message Processing API - Example Usage")
    print("=" * 50)
    
    # Test 1: Create a valid message
    print("1. Creating a valid system message...")
    message1 = {
        "message_id": "msg-demo-001",
        "session_id": "demo-session",
        "content": "Hello! Welcome to our chat system.",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system"
    }
    create_message(message1)
    
    # Test 2: Create a user message
    print("2. Creating a user message...")
    message2 = {
        "message_id": "msg-demo-002",
        "session_id": "demo-session", 
        "content": "Thank you! This is a great system.",
        "timestamp": "2023-06-15T14:31:00Z",
        "sender": "user"
    }
    create_message(message2)
    
    # Test 3: Try to create a message with inappropriate content
    print("3. Testing content filtering...")
    message3 = {
        "message_id": "msg-demo-003",
        "session_id": "demo-session",
        "content": "This message contains spam content that should be blocked",
        "timestamp": "2023-06-15T14:32:00Z",
        "sender": "user"
    }
    create_message(message3)
    
    # Test 4: Get all messages for the session
    print("4. Retrieving all messages for the session...")
    get_messages("demo-session")
    
    # Test 5: Get only user messages
    print("5. Retrieving only user messages...")
    get_messages("demo-session", sender="user")
    
    # Test 6: Test pagination
    print("6. Testing pagination (limit=1)...")
    get_messages("demo-session", limit=1, offset=0)
    
    # Test 7: Try duplicate message ID
    print("7. Testing duplicate message ID...")
    create_message(message1)  # Same as message1
    
    print("=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running with:")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"Error: {e}")