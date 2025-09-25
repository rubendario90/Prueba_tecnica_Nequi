from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, String, DateTime, Integer, Text, TypeDecorator
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UTCDateTime(TypeDecorator):
    """A DateTime column type that converts timezone-aware datetime objects to UTC naive datetime for SQLite compatibility."""
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        # Handle string input (ISO format)
        if isinstance(value, str):
            try:
                if value.endswith('Z'):
                    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:
                    value = datetime.fromisoformat(value)
            except ValueError:
                return value
        # Handle datetime objects
        if isinstance(value, datetime):
            if value.tzinfo is not None:
                utc_dt = value.astimezone(timezone.utc).replace(tzinfo=None)
                return utc_dt
            else:
                return value
        return value

    def process_result_value(self, value, dialect):
        return value

class SenderType(str, Enum):
    USER = "user"
    SYSTEM = "system"

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime

class MessageCreate(BaseModel):
    message_id: str = Field(..., description="Unique identifier for the message")
    session_id: str = Field(..., description="Session identifier")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp in ISO format")
    sender: SenderType = Field(..., description="Message sender: 'user' or 'system'")

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v

    @field_validator('message_id')
    @classmethod
    def validate_message_id(cls, v):
        if not v.strip():
            raise ValueError("Message ID cannot be empty")
        return v

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v):
        if not v.strip():
            raise ValueError("Session ID cannot be empty")
        return v

class MessageResponse(MessageCreate):
    metadata: MessageMetadata

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(UTCDateTime, nullable=False)
    sender = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
    processed_at = Column(UTCDateTime, nullable=False)