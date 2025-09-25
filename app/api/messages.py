from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.db.database import get_db
from app.core.errors import ApiError, ErrorResponse, ErrorDetail
from app.core.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/api", tags=["messages"])


class SuccessResponse(BaseModel):
    status: str = "success"
    data: MessageResponse


class MessagesListResponse(BaseModel):
    status: str = "success"
    data: List[MessageResponse]
    pagination: dict


@router.post("/messages", response_model=SuccessResponse)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new message.
    
    Validates the message format, processes the content, and stores it in the database.
    Returns the processed message with metadata.
    """
    try:
        service = MessageService(db)
        processed_message = service.process_message(message)

        return SuccessResponse(data=processed_message)

    except ApiError as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code=e.code,
                message=e.message,
                details=e.details
            ).dict()
        )
        raise HTTPException(
            status_code=e.status_code,
            detail=error_response.dict()
        )
    except Exception as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An internal server error occurred",
                details=str(e)
            ).dict()
        )
        raise HTTPException(
            status_code=500,
            detail=error_response.dict()
        )


@router.get("/messages/{session_id}", response_model=MessagesListResponse)
async def get_messages(
    session_id: str,
    sender: Optional[str] = Query(None, description="Filter by sender: 'user' or 'system'"),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Number of messages per page"),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
    db: Session = Depends(get_db)
):
    """
    Get messages for a specific session.
    
    Supports pagination and filtering by sender.
    """
    try:
        service = MessageService(db)
        messages = service.get_messages_by_session(
            session_id=session_id,
            sender=sender,
            limit=limit,
            offset=offset
        )

        pagination = {
            "limit": limit,
            "offset": offset,
            "total": len(messages)
        }

        return MessagesListResponse(
            data=messages,
            pagination=pagination
        )

    except ApiError as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code=e.code,
                message=e.message,
                details=e.details
            ).dict()
        )
        raise HTTPException(
            status_code=e.status_code,
            detail=error_response.dict()
        )
    except Exception as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An internal server error occurred",
                details=str(e)
            ).dict()
        )
        raise HTTPException(
            status_code=500,
            detail=error_response.dict()
        )