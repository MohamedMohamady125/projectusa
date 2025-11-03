"""
Document model for athlete document management.
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


class DocumentType(str, PyEnum):
    """Document type enumeration."""
    TRANSCRIPT = "transcript"
    TEST_SCORE = "test_score"
    SWIMMING_CERT = "swimming_cert"
    PASSPORT = "passport"
    VISA = "visa"
    MEDICAL = "medical"
    FINANCIAL = "financial"
    OTHER = "other"


class Document(Base):
    """Document model for storing athlete documents."""

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(DocumentType, name='document_type', values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    expires_at = Column(Date, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    translation_url = Column(Text, nullable=True)
    document_metadata = Column(JSONB, default=dict, nullable=False)  # Renamed from 'metadata' to avoid SQLAlchemy reserved name
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="documents")
    verifier = relationship("User", foreign_keys=[verified_by])

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, name={self.name}, type={self.type})>"

    @property
    def is_expired(self) -> bool:
        """Check if document is expired."""
        if self.expires_at:
            return date.today() > self.expires_at
        return False
