"""
User schemas for authentication and user management.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr, Field, field_validator
from app.models.user import UserRole
from app.schemas.base import BaseSchema, IDSchema, TimestampSchema


class UserBase(BaseSchema):
    """Base user schema with common fields."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = UserRole.ATHLETE

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseSchema):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseSchema):
    """Schema for updating user."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase, IDSchema, TimestampSchema):
    """Schema for user response."""
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None


class UserInDB(UserResponse):
    """Schema for user in database (includes password hash)."""
    password_hash: str
    verification_token: Optional[str] = None
    reset_password_token: Optional[str] = None
    reset_password_expires: Optional[datetime] = None


class PasswordReset(BaseSchema):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Schema for password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class EmailVerification(BaseSchema):
    """Schema for email verification."""
    token: str


class ChangePassword(BaseSchema):
    """Schema for changing password."""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
