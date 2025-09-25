from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    character_count = Column(Integer, nullable=False)
    processed_at = Column(DateTime, nullable=False)