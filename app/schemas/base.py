"""
Base Pydantic schemas with common fields and configurations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    created_at: datetime
    updated_at: datetime


class IDSchema(BaseSchema):
    """Schema with ID field."""
    id: UUID


class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = 0
    limit: int = 20


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    total: int
    skip: int
    limit: int
    items: list


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class TokenResponse(BaseModel):
    """Token response for authentication."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
