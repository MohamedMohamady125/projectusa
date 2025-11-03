"""
Custom exception classes for the application.
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base exception class for API errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthenticationError(BaseAPIException):
    """Exception raised for authentication failures."""

    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(BaseAPIException):
    """Exception raised for authorization failures."""

    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class NotFoundError(BaseAPIException):
    """Exception raised when a resource is not found."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ConflictError(BaseAPIException):
    """Exception raised for resource conflicts."""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class ValidationError(BaseAPIException):
    """Exception raised for validation errors."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class BadRequestError(BaseAPIException):
    """Exception raised for bad requests."""

    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class InternalServerError(BaseAPIException):
    """Exception raised for internal server errors."""

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ServiceUnavailableError(BaseAPIException):
    """Exception raised when a service is unavailable."""

    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )


class RateLimitError(BaseAPIException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        )


# Domain-specific exceptions
class UserNotFoundError(NotFoundError):
    """Exception raised when a user is not found."""

    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail)


class AthleteNotFoundError(NotFoundError):
    """Exception raised when an athlete profile is not found."""

    def __init__(self, detail: str = "Athlete profile not found"):
        super().__init__(detail=detail)


class SchoolNotFoundError(NotFoundError):
    """Exception raised when a school is not found."""

    def __init__(self, detail: str = "School not found"):
        super().__init__(detail=detail)


class TaskNotFoundError(NotFoundError):
    """Exception raised when a task is not found."""

    def __init__(self, detail: str = "Task not found"):
        super().__init__(detail=detail)


class DocumentNotFoundError(NotFoundError):
    """Exception raised when a document is not found."""

    def __init__(self, detail: str = "Document not found"):
        super().__init__(detail=detail)


class InvalidCredentialsError(AuthenticationError):
    """Exception raised for invalid login credentials."""

    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(detail=detail)


class EmailAlreadyExistsError(ConflictError):
    """Exception raised when email already exists."""

    def __init__(self, detail: str = "Email already registered"):
        super().__init__(detail=detail)


class InactiveUserError(AuthenticationError):
    """Exception raised when user account is inactive."""

    def __init__(self, detail: str = "User account is inactive"):
        super().__init__(detail=detail)


class UnverifiedUserError(AuthenticationError):
    """Exception raised when user email is not verified."""

    def __init__(self, detail: str = "Email not verified"):
        super().__init__(detail=detail)


class InvalidTokenError(AuthenticationError):
    """Exception raised for invalid tokens."""

    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(detail=detail)


class FileUploadError(BadRequestError):
    """Exception raised for file upload errors."""

    def __init__(self, detail: str = "File upload failed"):
        super().__init__(detail=detail)


class FileSizeExceededError(BadRequestError):
    """Exception raised when file size exceeds limit."""

    def __init__(self, detail: str = "File size exceeds maximum allowed size"):
        super().__init__(detail=detail)


class InvalidFileTypeError(BadRequestError):
    """Exception raised for invalid file types."""

    def __init__(self, detail: str = "Invalid file type"):
        super().__init__(detail=detail)
