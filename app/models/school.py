"""
School, coach, and team ranking models.
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


class DivisionType(str, PyEnum):
    """Division type enumeration."""
    D1 = "D1"
    D1_MID_MAJOR = "D1_MID_MAJOR"
    D2 = "D2"
    D3 = "D3"
    NAIA = "NAIA"
    NJCAA = "NJCAA"


class School(Base):
    """School model."""

    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(255), nullable=False)
    division = Column(Enum(DivisionType, name='division_type', values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    state = Column(String(50), nullable=True, index=True)
    city = Column(String(100), nullable=True)
    conference = Column(String(100), nullable=True)
    school_website = Column(Text, nullable=True)
    swim_website_men = Column(Text, nullable=True)
    swim_website_women = Column(Text, nullable=True)
    midseason_meet_url_men = Column(Text, nullable=True)
    midseason_meet_url_women = Column(Text, nullable=True)
    conference_meet_url_men = Column(Text, nullable=True)
    conference_meet_url_women = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    enrollment = Column(Integer, nullable=True)
    public_private = Column(String(20), nullable=True)
    international_students_percentage = Column(Numeric(5, 2), nullable=True)
    average_sat = Column(Integer, nullable=True)
    average_act = Column(Integer, nullable=True)
    average_gpa = Column(Numeric(3, 2), nullable=True)
    tuition_in_state = Column(Integer, nullable=True)
    tuition_out_state = Column(Integer, nullable=True)
    room_board = Column(Integer, nullable=True)
    has_mens_team = Column(Boolean, default=True, nullable=False)
    has_womens_team = Column(Boolean, default=True, nullable=False)
    mens_scholarships = Column(Integer, nullable=True)
    womens_scholarships = Column(Integer, nullable=True)
    mens_ranking = Column(Integer, nullable=True)
    womens_ranking = Column(Integer, nullable=True)
    mens_ranking_points = Column(Numeric(10, 2), nullable=True)
    womens_ranking_points = Column(Numeric(10, 2), nullable=True)
    recruiting_questionnaire_url = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    images = Column(JSONB, default=list, nullable=False)
    facilities_info = Column(Text, nullable=True)
    academic_support = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    coaches = relationship("Coach", back_populates="school", cascade="all, delete-orphan")
    team_rankings = relationship("TeamRanking", back_populates="school", cascade="all, delete-orphan")
    recruitment_tracking = relationship("RecruitmentTracking", back_populates="school")
    communications = relationship("Communication", back_populates="school")
    tasks = relationship("Task", back_populates="related_school")

    def __repr__(self) -> str:
        return f"<School(id={self.id}, name={self.name}, division={self.division})>"


class Coach(Base):
    """Coach model."""

    __tablename__ = "coaches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=True)  # 'Head Coach', 'Assistant Coach', etc.
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    is_mens_coach = Column(Boolean, default=True, nullable=False)
    is_womens_coach = Column(Boolean, default=True, nullable=False)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(Text, nullable=True)
    preferred_contact_method = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    school = relationship("School", back_populates="coaches")
    communications = relationship("Communication", back_populates="coach")

    def __repr__(self) -> str:
        return f"<Coach(id={self.id}, name={self.name}, school_id={self.school_id})>"


class TeamRanking(Base):
    """Team ranking model."""

    __tablename__ = "team_rankings"
    __table_args__ = (
        UniqueConstraint('school_id', 'division', 'season', 'gender', name='uq_team_ranking'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id", ondelete="CASCADE"), nullable=False, index=True)
    division = Column(Enum(DivisionType, name='division_type', values_callable=lambda x: [e.value for e in x]), nullable=False, index=True)
    ranking = Column(Integer, nullable=False)
    season = Column(String(20), nullable=True)  # '2024-2025'
    gender = Column(String(10), nullable=True)  # 'men', 'women'
    total_points = Column(Numeric(10, 2), nullable=True)
    conference_rank = Column(Integer, nullable=True)
    last_updated = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    school = relationship("School", back_populates="team_rankings")

    def __repr__(self) -> str:
        return f"<TeamRanking(id={self.id}, school_id={self.school_id}, ranking={self.ranking})>"
