from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    status: str = "error"
    error: dict


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None


class ApiError(Exception):
    def __init__(self, code: str, message: str, details: Optional[str] = None, status_code: int = 400):
        self.code = code
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ApiError):
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__("INVALID_FORMAT", message, details, 400)


class NotFoundError(ApiError):
    def __init__(self, message: str = "Resource not found", details: Optional[str] = None):
        super().__init__("NOT_FOUND", message, details, 404)


class DuplicateError(ApiError):
    def __init__(self, message: str = "Resource already exists", details: Optional[str] = None):
        super().__init__("DUPLICATE_RESOURCE", message, details, 409)