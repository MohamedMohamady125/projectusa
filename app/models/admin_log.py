"""
Admin activity log model for audit trail.
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship

from app.db.base import Base


class AdminActivityLog(Base):
    """Admin activity log model."""

    __tablename__ = "admin_activity_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=True)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    changes = Column(JSONB, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    admin = relationship("User", back_populates="admin_activities", foreign_keys=[admin_id])

    def __repr__(self) -> str:
        return f"<AdminActivityLog(id={self.id}, admin_id={self.admin_id}, action={self.action})>"
