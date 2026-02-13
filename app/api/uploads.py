import os
import uuid
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
    original_filename: str
    size: int
    content_type: str


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks."""
    # Get just the basename, removing any path components
    safe_name = os.path.basename(filename)
    # Remove any potentially dangerous characters
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._- ")
    # Generate unique filename with UUID prefix to prevent collisions
    name, ext = os.path.splitext(safe_name)
    unique_name = f"{uuid.uuid4().hex[:8]}_{name}{ext}"
    return unique_name


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

        # Sanitize filename to prevent path traversal
        safe_filename = sanitize_filename(file.filename)

        # Create upload directory if it doesn't exist
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(exist_ok=True)

        # Save file in chunks to avoid memory issues with large files
        file_path = upload_path / safe_filename
        file_size = 0
        chunk_size = 1024 * 1024  # 1 MB chunks

        with open(file_path, "wb") as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                
                file_size += len(chunk)
                
                # Check size limit while streaming
                if file_size > MAX_FILE_SIZE:
                    # Clean up partial file
                    f.close()
                    file_path.unlink(missing_ok=True)
                    
                    error_response = ErrorResponse(
                        error=ErrorDetail(
                            code="INVALID_FORMAT",
                            message="File size exceeds maximum allowed",
                            details=f"Maximum file size: {MAX_FILE_SIZE / (1024 * 1024):.0f} MB"
                        ).model_dump()
                    )
                    raise HTTPException(status_code=400, detail=error_response.model_dump())
                
                f.write(chunk)

        return UploadResponse(
            message="Video uploaded successfully",
            filename=safe_filename,
            original_filename=file.filename,
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

        # Sanitize filename to prevent path traversal
        safe_filename = sanitize_filename(file.filename)

        # Create upload directory if it doesn't exist
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(exist_ok=True)

        # Save file in chunks to avoid memory issues with large files
        file_path = upload_path / safe_filename
        file_size = 0
        chunk_size = 1024 * 1024  # 1 MB chunks

        with open(file_path, "wb") as f:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                
                file_size += len(chunk)
                
                # Check size limit while streaming
                if file_size > MAX_FILE_SIZE:
                    # Clean up partial file
                    f.close()
                    file_path.unlink(missing_ok=True)
                    
                    error_response = ErrorResponse(
                        error=ErrorDetail(
                            code="INVALID_FORMAT",
                            message="File size exceeds maximum allowed",
                            details=f"Maximum file size: {MAX_FILE_SIZE / (1024 * 1024):.0f} MB"
                        ).model_dump()
                    )
                    raise HTTPException(status_code=400, detail=error_response.model_dump())
                
                f.write(chunk)

        return UploadResponse(
            message="File uploaded successfully",
            filename=safe_filename,
            original_filename=file.filename,
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
