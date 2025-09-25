from datetime import datetime
from pydantic import BaseModel


class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: datetime