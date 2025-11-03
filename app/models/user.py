"""
User model for authentication and user management.
"""
from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, PyEnum):
    """User role enumeration."""
    ATHLETE = "athlete"
    ADMIN = "admin"
    COACH = "coach"
    PARENT = "parent"


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name='user_role', values_callable=lambda x: [e.value for e in x]), default=UserRole.ATHLETE, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), nullable=True)
    reset_password_token = Column(String(255), nullable=True)
    reset_password_expires = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    athlete_profile = relationship("AthleteProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    admin_activities = relationship("AdminActivityLog", back_populates="admin", foreign_keys="AdminActivityLog.admin_id")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
