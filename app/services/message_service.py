from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.message import MessageCreate, MessageResponse, MessageMetadata, Message
from app.repository.message_repository import MessageRepository
from app.core.config import INAPPROPRIATE_WORDS
from app.core.errors import ValidationError


class MessageService:
    def __init__(self, db: Session):
        self.repository = MessageRepository(db)
        self.db = db

    def process_message(self, message_data: MessageCreate) -> MessageResponse:
        """
        Process and store a message with validation and content filtering.
        """
        # Validate content for inappropriate words
        self._validate_content(message_data.content)
        
        # Calculate metadata
        word_count = len(message_data.content.strip().split())
        character_count = len(message_data.content)
        processed_at = datetime.now(timezone.utc)
        
        # Store message
        db_message = self.repository.create_message(
            message_data=message_data,
            word_count=word_count,
            character_count=character_count,
            processed_at=processed_at
        )
        
        # Create response with metadata
        metadata = MessageMetadata(
            word_count=word_count,
            character_count=character_count,
            processed_at=processed_at
        )
        
        return MessageResponse(
            message_id=db_message.message_id,
            session_id=db_message.session_id,
            content=db_message.content,
            timestamp=db_message.timestamp,
            sender=db_message.sender,
            metadata=metadata
        )

    def get_messages_by_session(
        self, 
        session_id: str, 
        sender: Optional[str] = None,
        limit: int = 10, 
        offset: int = 0
    ) -> List[MessageResponse]:
        """
        Retrieve messages for a session with optional filtering and pagination.
        """
        if sender and sender not in ["user", "system"]:
            raise ValidationError("Sender must be 'user' or 'system'")
            
        messages = self.repository.get_messages_by_session(
            session_id=session_id,
            sender=sender,
            limit=limit,
            offset=offset
        )
        
        return [self._convert_to_response(msg) for msg in messages]

    def _validate_content(self, content: str) -> None:
        """
        Validate message content for inappropriate words.
        """
        content_lower = content.lower()
        for word in INAPPROPRIATE_WORDS:
            if word in content_lower:
                raise ValidationError(
                    "Message contains inappropriate content",
                    f"The word '{word}' is not allowed"
                )

    def _convert_to_response(self, db_message: Message) -> MessageResponse:
        """
        Convert database message to response model.
        """
        metadata = MessageMetadata(
            word_count=db_message.word_count,
            character_count=db_message.character_count,
            processed_at=db_message.processed_at
        )
        
        return MessageResponse(
            message_id=db_message.message_id,
            session_id=db_message.session_id,
            content=db_message.content,
            timestamp=db_message.timestamp,
            sender=db_message.sender,
            metadata=metadata
        )