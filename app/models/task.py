"""
Task model for athlete task management.
"""
from datetime import date, datetime
from enum import Enum as PyEnum
from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, Date, DateTime, Enum, ForeignKey,
    Integer, String, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class TaskStatus(str, PyEnum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskCategory(str, PyEnum):
    """Task category enumeration."""
    VISA = "visa"
    NCAA = "ncaa"
    SEVIS = "sevis"
    ACADEMIC = "academic"
    SWIMMING = "swimming"
    FINANCIAL = "financial"
    CUSTOM = "custom"


class Task(Base):
    """Task model for athlete task management."""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(TaskCategory, name='task_category', values_callable=lambda x: [e.value for e in x]), nullable=False)
    status = Column(Enum(TaskStatus, name='task_status', values_callable=lambda x: [e.value for e in x]), default=TaskStatus.PENDING, nullable=False, index=True)
    priority = Column(Integer, default=3, nullable=False)  # 1 (highest) to 5 (lowest)
    due_date = Column(Date, nullable=True, index=True)
    completed_at = Column(DateTime, nullable=True)
    is_system_generated = Column(Boolean, default=False, nullable=False)
    related_school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=True)
    reminder_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    attachments = Column(JSONB, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="tasks")
    related_school = relationship("School", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date and self.status != TaskStatus.COMPLETED:
            return date.today() > self.due_date
        return False
