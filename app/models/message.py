
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class MessageCreate(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str  # "user" o "system"

class MessageResponse(MessageCreate):
    metadata: Optional[Dict] = None