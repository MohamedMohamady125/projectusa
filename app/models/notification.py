"""
Notification model for user notifications.
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, String, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class Notification(Base):
    """Notification model."""

    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    type = Column(String(50), nullable=True)  # 'task_due', 'new_message', 'deadline', etc.
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True)
    action_url = Column(Text, nullable=True)
    notification_metadata = Column(JSONB, default=dict, nullable=False)  # Renamed from 'metadata' to avoid SQLAlchemy reserved name
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, user_id={self.user_id}, title={self.title})>"
