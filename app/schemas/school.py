"""
School, coach, and team ranking schemas.
"""
from datetime import date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import Field
from app.models.school import DivisionType
from app.schemas.base import BaseSchema, IDSchema, TimestampSchema


class SchoolBase(BaseSchema):
    """Base school schema."""
    name: str = Field(..., min_length=1, max_length=255)
    division: DivisionType
    state: Optional[str] = None
    city: Optional[str] = None
    conference: Optional[str] = None
    school_website: Optional[str] = None
    swim_website_men: Optional[str] = None
    swim_website_women: Optional[str] = None
    midseason_meet_url_men: Optional[str] = None
    midseason_meet_url_women: Optional[str] = None
    conference_meet_url_men: Optional[str] = None
    conference_meet_url_women: Optional[str] = None
    description: Optional[str] = None
    enrollment: Optional[int] = Field(None, gt=0)
    public_private: Optional[str] = None
    international_students_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    average_sat: Optional[int] = Field(None, ge=400, le=1600)
    average_act: Optional[int] = Field(None, ge=1, le=36)
    average_gpa: Optional[Decimal] = Field(None, ge=0, le=4)
    tuition_in_state: Optional[int] = Field(None, ge=0)
    tuition_out_state: Optional[int] = Field(None, ge=0)
    room_board: Optional[int] = Field(None, ge=0)
    has_mens_team: bool = True
    has_womens_team: bool = True
    mens_scholarships: Optional[int] = Field(None, ge=0)
    womens_scholarships: Optional[int] = Field(None, ge=0)
    mens_ranking: Optional[int] = Field(None, ge=1)
    womens_ranking: Optional[int] = Field(None, ge=1)
    mens_ranking_points: Optional[Decimal] = Field(None, ge=0)
    womens_ranking_points: Optional[Decimal] = Field(None, ge=0)
    recruiting_questionnaire_url: Optional[str] = None
    logo_url: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    facilities_info: Optional[str] = None
    academic_support: Optional[str] = None


class SchoolCreate(SchoolBase):
    """Schema for creating school."""
    pass


class SchoolUpdate(BaseSchema):
    """Schema for updating school."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    division: Optional[DivisionType] = None
    state: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None


class SchoolResponse(SchoolBase, IDSchema, TimestampSchema):
    """Schema for school response."""
    pass


class CoachBase(BaseSchema):
    """Base coach schema."""
    name: str = Field(..., min_length=1, max_length=255)
    role: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_mens_coach: bool = True
    is_womens_coach: bool = True
    bio: Optional[str] = None


class CoachCreate(CoachBase):
    """Schema for creating coach."""
    school_id: UUID


class CoachResponse(CoachBase, IDSchema, TimestampSchema):
    """Schema for coach response."""
    school_id: UUID
