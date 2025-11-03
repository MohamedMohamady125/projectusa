"""
Task schemas for request/response validation.
"""
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    priority: int = Field(3, ge=1, le=5)
    due_date: Optional[date] = None
    related_school_id: Optional[UUID] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: UUID
    athlete_id: UUID
    status: str
    completed_at: Optional[datetime] = None
    is_system_generated: bool
    reminder_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
