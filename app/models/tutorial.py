"""
Video tutorial and progress tracking models.
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey,
    Integer, String, Text, UniqueConstraint, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class VideoTutorial(Base):
    """Video tutorial model."""

    __tablename__ = "video_tutorials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    video_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    order_index = Column(Integer, nullable=True)
    is_premium = Column(Boolean, default=False, nullable=False)
    transcript_es = Column(Text, nullable=True)
    transcript_en = Column(Text, nullable=True)
    pdf_resources = Column(JSONB, default=list, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    view_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tutorial_progress = relationship("TutorialProgress", back_populates="tutorial", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<VideoTutorial(id={self.id}, title={self.title})>"


class TutorialProgress(Base):
    """Tutorial progress tracking model."""

    __tablename__ = "tutorial_progress"
    __table_args__ = (
        UniqueConstraint('athlete_id', 'tutorial_id', name='uq_tutorial_progress'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    athlete_id = Column(UUID(as_uuid=True), ForeignKey("athlete_profiles.id", ondelete="CASCADE"), nullable=False)
    tutorial_id = Column(UUID(as_uuid=True), ForeignKey("video_tutorials.id", ondelete="CASCADE"), nullable=False)
    watched_seconds = Column(Integer, default=0, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete = relationship("AthleteProfile", back_populates="tutorial_progress")
    tutorial = relationship("VideoTutorial", back_populates="tutorial_progress")

    def __repr__(self) -> str:
        return f"<TutorialProgress(id={self.id}, athlete_id={self.athlete_id}, tutorial_id={self.tutorial_id}, completed={self.completed})>"

    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.tutorial and self.tutorial.duration_seconds:
            return min((self.watched_seconds / self.tutorial.duration_seconds) * 100, 100)
        return 0.0
