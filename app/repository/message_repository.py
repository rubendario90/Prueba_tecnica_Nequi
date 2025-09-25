from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.message import Message, MessageCreate
from app.core.errors import DuplicateError, NotFoundError


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message_data: MessageCreate, word_count: int, character_count: int, processed_at) -> Message:
        """
        Create a new message in the database.
        """
        try:
            db_message = Message(
                message_id=message_data.message_id,
                session_id=message_data.session_id,
                content=message_data.content,
                timestamp=message_data.timestamp,
                sender=message_data.sender.value,
                word_count=word_count,
                character_count=character_count,
                processed_at=processed_at
            )
            self.db.add(db_message)
            self.db.commit()
            self.db.refresh(db_message)
            return db_message
        except IntegrityError:
            self.db.rollback()
            raise DuplicateError(f"Message with ID {message_data.message_id} already exists")

    def get_messages_by_session(
        self, 
        session_id: str, 
        sender: Optional[str] = None,
        limit: int = 10, 
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages by session ID with optional filtering and pagination.
        """
        query = self.db.query(Message).filter(Message.session_id == session_id)

        if sender:
            query = query.filter(Message.sender == sender)

        messages = query.order_by(Message.timestamp.desc()).offset(offset).limit(limit).all()
        return messages

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """
        Get a single message by its ID.
        """
        return self.db.query(Message).filter(Message.message_id == message_id).first()

    def message_exists(self, message_id: str) -> bool:
        """
        Check if a message exists by its ID.
        """
        return self.db.query(Message).filter(Message.message_id == message_id).first() is not None