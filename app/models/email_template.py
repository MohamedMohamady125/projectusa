"""
Email template model for reusable email templates.
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base


class EmailTemplate(Base):
    """Email template model."""

    __tablename__ = "email_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    subject_en = Column(String(255), nullable=True)
    subject_es = Column(String(255), nullable=True)
    content_en = Column(Text, nullable=True)
    content_es = Column(Text, nullable=True)
    variables = Column(JSONB, default=list, nullable=False)  # List of variables like {{coach_name}}, {{school_name}}
    is_active = Column(Boolean, default=True, nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<EmailTemplate(id={self.id}, name={self.name})>"
