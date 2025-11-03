"""
Athlete profile and swimming time schemas.
"""
from datetime import date
from decimal import Decimal
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import Field
from app.models.athlete import SwimmingCourse
from app.schemas.base import BaseSchema, IDSchema, TimestampSchema


class AthleteProfileBase(BaseSchema):
    """Base athlete profile schema."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    nationality: str = "Spain"
    current_city: Optional[str] = None
    phone_number: Optional[str] = None
    height_cm: Optional[int] = Field(None, gt=0, le=300)
    weight_kg: Optional[Decimal] = Field(None, gt=0, le=200)
    graduation_date: date
    current_school: Optional[str] = None
    gpa: Optional[Decimal] = Field(None, ge=0, le=4)
    sat_score: Optional[int] = Field(None, ge=400, le=1600)
    act_score: Optional[int] = Field(None, ge=1, le=36)
    toefl_score: Optional[int] = Field(None, ge=0, le=120)
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    recruiting_video_url: Optional[str] = None
    ncaa_id: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)


class AthleteProfileCreate(AthleteProfileBase):
    """Schema for creating athlete profile."""
    user_id: UUID


class AthleteProfileUpdate(BaseSchema):
    """Schema for updating athlete profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    current_city: Optional[str] = None
    phone_number: Optional[str] = None
    height_cm: Optional[int] = Field(None, gt=0, le=300)
    weight_kg: Optional[Decimal] = Field(None, gt=0, le=200)
    graduation_date: Optional[date] = None
    current_school: Optional[str] = None
    gpa: Optional[Decimal] = Field(None, ge=0, le=4)
    sat_score: Optional[int] = Field(None, ge=400, le=1600)
    act_score: Optional[int] = Field(None, ge=1, le=36)
    toefl_score: Optional[int] = Field(None, ge=0, le=120)
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None
    recruiting_video_url: Optional[str] = None
    ncaa_id: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class AthleteProfileResponse(AthleteProfileBase, IDSchema, TimestampSchema):
    """Schema for athlete profile response."""
    user_id: UUID


class SwimmingTimeBase(BaseSchema):
    """Base swimming time schema."""
    event: str = Field(..., min_length=1, max_length=100)
    time_seconds: Decimal = Field(..., gt=0)
    course: SwimmingCourse
    meet_name: Optional[str] = None
    meet_date: Optional[date] = None
    is_official: bool = False
    video_url: Optional[str] = None
    verification_url: Optional[str] = None


class SwimmingTimeCreate(SwimmingTimeBase):
    """Schema for creating swimming time."""
    athlete_id: UUID


class SwimmingTimeUpdate(BaseSchema):
    """Schema for updating swimming time."""
    event: Optional[str] = Field(None, min_length=1, max_length=100)
    time_seconds: Optional[Decimal] = Field(None, gt=0)
    course: Optional[SwimmingCourse] = None
    meet_name: Optional[str] = None
    meet_date: Optional[date] = None
    is_official: Optional[bool] = None
    video_url: Optional[str] = None
    verification_url: Optional[str] = None


class SwimmingTimeResponse(SwimmingTimeBase, IDSchema, TimestampSchema):
    """Schema for swimming time response."""
    athlete_id: UUID
    rank_division1: Optional[int] = None
    rank_division2: Optional[int] = None
    rank_division3: Optional[int] = None
