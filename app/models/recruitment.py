"""
Recruitment tracking and communication models.
"""
from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PyEnum
from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, Date, DateTime, Enum, ForeignKey,
    Integer, Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class RecruitmentStatus(str, PyEnum):
    """Recruitment status enumeration."""
    RESEARCHING = "researching"
    INITIAL_CONTACT = "initial_contact"
    ACTIVE_COMMUNICATION = "active_communication"
    VISIT_SCHEDULED = "visit_scheduled"
    OFFER_RECEIVED = "offer_received"
    COMMITTED = "committed"
    DECLINED = "declined"


class CommunicationType(str, PyEnum):
    """Communication type enumeration."""
    EMAIL_SENT = "email_sent"
    EMAIL_RECEIVED = "email_received"
    CALL = "call"
    TEXT = "text"
    VISIT = "visit"
    OTHER = "other"


class RecruitmentTracking(Base):
    """Recruitment tracking model."""

    __tablename__ = "recruitment_tracking"
    __table_args__ = (
        UniqueConstraint('athlete_id', 'school_id', name='uq_recruitment_tracking'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(RecruitmentStatus, name='recruitment_status', values_callable=lambda x: [e.value for e in x]), default=RecruitmentStatus.RESEARCHING, nullable=False, index=True)
    interest_level = Column(Integer, nullable=True)  # 1-10 scale
    coach_interest_level = Column(Integer, nullable=True)  # 1-10 scale
    last_contact_date = Column(DateTime, nullable=True)
    next_action_date = Column(Date, nullable=True)
    scholarship_offered = Column(Numeric(10, 2), nullable=True)
    scholarship_details = Column(Text, nullable=True)
    official_visit_date = Column(Date, nullable=True)
    unofficial_visit_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="recruitment_tracking")
    school = relationship("School", back_populates="recruitment_tracking")

    def __repr__(self) -> str:
        return f"<RecruitmentTracking(id={self.id}, athlete_id={self.athlete_id}, school_id={self.school_id}, status={self.status})>"


class Communication(Base):
    """Communication model for tracking athlete-coach interactions."""

    __tablename__ = "communications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=True, index=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coaches.id"), nullable=True)
    type = Column(Enum(CommunicationType, name='communication_type', values_callable=lambda x: [e.value for e in x]), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    is_inbound = Column(Boolean, default=False, nullable=False)
    email_thread_id = Column(String(255), nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    response_received = Column(Boolean, default=False, nullable=False)
    attachments = Column(JSONB, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="communications")
    school = relationship("School", back_populates="communications")
    coach = relationship("Coach", back_populates="communications")

    def __repr__(self) -> str:
        return f"<Communication(id={self.id}, type={self.type}, athlete_id={self.athlete_id})>"
