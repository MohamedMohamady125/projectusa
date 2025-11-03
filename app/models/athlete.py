"""
Athlete profile and swimming times models.
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


class SwimmingCourse(str, PyEnum):
    """Swimming course enumeration."""
    SCY = "SCY"  # Short Course Yards
    SCM = "SCM"  # Short Course Meters
    LCM = "LCM"  # Long Course Meters


class AthleteProfile(Base):
    """Athlete profile model."""

    __tablename__ = "athlete_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    nationality = Column(String(100), default="Spain")
    current_city = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)
    height_cm = Column(Integer, nullable=True)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    graduation_date = Column(Date, nullable=False, index=True)
    current_school = Column(String(255), nullable=True)
    gpa = Column(Numeric(3, 2), nullable=True)
    sat_score = Column(Integer, nullable=True)
    act_score = Column(Integer, nullable=True)
    toefl_score = Column(Integer, nullable=True)
    profile_image_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    recruiting_video_url = Column(Text, nullable=True)
    ncaa_id = Column(String(100), nullable=True)
    preferences = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="athlete_profile")
    swimming_times = relationship("SwimmingTime", back_populates="athlete", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="athlete", cascade="all, delete-orphan")
    recruitment_tracking = relationship("RecruitmentTracking", back_populates="athlete", cascade="all, delete-orphan")
    communications = relationship("Communication", back_populates="athlete", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="athlete", cascade="all, delete-orphan")
    tutorial_progress = relationship("TutorialProgress", back_populates="athlete", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AthleteProfile(id={self.id}, name={self.first_name} {self.last_name})>"

    @property
    def full_name(self) -> str:
        """Get full name of athlete."""
        return f"{self.first_name} {self.last_name}"


class SwimmingTime(Base):
    """Swimming time record model."""

    __tablename__ = "swimming_times"
    __table_args__ = (
        UniqueConstraint('athlete_id', 'event', 'course', 'time_seconds', name='uq_swimming_time'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    event = Column(String(100), nullable=False, index=True)  # '50 Free', '100 Fly', etc.
    time_seconds = Column(Numeric(8, 2), nullable=False)
    course = Column(Enum(SwimmingCourse, name='swimming_course', values_callable=lambda x: [e.value for e in x]), nullable=False)
    meet_name = Column(String(255), nullable=True)
    meet_date = Column(Date, nullable=True)
    is_official = Column(Boolean, default=False, nullable=False)
    video_url = Column(Text, nullable=True)
    verification_url = Column(Text, nullable=True)
    rank_division1 = Column(Integer, nullable=True)
    rank_division2 = Column(Integer, nullable=True)
    rank_division3 = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="swimming_times")

    def __repr__(self) -> str:
        return f"<SwimmingTime(id={self.id}, event={self.event}, time={self.time_seconds}, course={self.course})>"

    @property
    def time_formatted(self) -> str:
        """Format time as MM:SS.ms"""
        total_seconds = float(self.time_seconds)
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:05.2f}"
