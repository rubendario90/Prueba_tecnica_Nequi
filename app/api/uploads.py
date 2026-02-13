import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pydantic import BaseModel

from app.core.config import (
    MAX_FILE_SIZE,
    ALLOWED_FILE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    UPLOAD_DIR
)
from app.core.errors import ValidationError, ErrorResponse, ErrorDetail

router = APIRouter(prefix="/api", tags=["uploads"])


class UploadResponse(BaseModel):
    status: str = "success"
    message: str
    filename: str
    size: int
    content_type: str


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension against allowed list."""
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions


def validate_file_size(file_size: int) -> bool:
    """Validate file size is within limits."""
    return file_size <= MAX_FILE_SIZE


@router.post("/upload/video", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload a video file.

    Validates video format, size limits, and stores the file.
    Returns upload confirmation with file metadata.
    """
    try:
        # Validate file was provided
        if not file or not file.filename:
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="No file provided",
                    details="A video file must be uploaded"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Validate file extension
        if not validate_file_extension(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="Invalid video format",
                    details=f"Allowed formats: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Read file content to get size
        file_content = await file.read()
        file_size = len(file_content)

        # Validate file size
        if not validate_file_size(file_size):
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="File size exceeds maximum allowed",
                    details=f"Maximum file size: {MAX_FILE_SIZE / (1024 * 1024):.0f} MB"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Create upload directory if it doesn't exist
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(exist_ok=True)

        # Save file
        file_path = upload_path / file.filename
        with open(file_path, "wb") as f:
            f.write(file_content)

        return UploadResponse(
            message="Video uploaded successfully",
            filename=file.filename,
            size=file_size,
            content_type=file.content_type or "application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An error occurred while uploading the file",
                details=str(e)
            ).model_dump()
        )
        raise HTTPException(
            status_code=500,
            detail=error_response.model_dump()
        )


@router.post("/upload/file", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload a file.

    Validates file format, size limits, and stores the file.
    Returns upload confirmation with file metadata.
    """
    try:
        # Validate file was provided
        if not file or not file.filename:
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="No file provided",
                    details="A file must be uploaded"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Validate file extension
        if not validate_file_extension(file.filename, ALLOWED_FILE_EXTENSIONS):
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="Invalid file format",
                    details=f"Allowed formats: {', '.join(ALLOWED_FILE_EXTENSIONS)}"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Read file content to get size
        file_content = await file.read()
        file_size = len(file_content)

        # Validate file size
        if not validate_file_size(file_size):
            error_response = ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message="File size exceeds maximum allowed",
                    details=f"Maximum file size: {MAX_FILE_SIZE / (1024 * 1024):.0f} MB"
                ).model_dump()
            )
            raise HTTPException(status_code=400, detail=error_response.model_dump())

        # Create upload directory if it doesn't exist
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(exist_ok=True)

        # Save file
        file_path = upload_path / file.filename
        with open(file_path, "wb") as f:
            f.write(file_content)

        return UploadResponse(
            message="File uploaded successfully",
            filename=file.filename,
            size=file_size,
            content_type=file.content_type or "application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        error_response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="An error occurred while uploading the file",
                details=str(e)
            ).model_dump()
        )
        raise HTTPException(
            status_code=500,
            detail=error_response.model_dump()
        )
