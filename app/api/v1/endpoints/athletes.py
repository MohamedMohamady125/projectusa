"""
Athlete profile and swimming times endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.core.dependencies import get_db, get_current_athlete
from app.models.user import User
from app.schemas.athlete import (
    AthleteProfileCreate,
    AthleteProfileUpdate,
    AthleteProfileResponse,
    SwimmingTimeCreate,
    SwimmingTimeResponse
)

router = APIRouter()


@router.post("/profile", response_model=AthleteProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: AthleteProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_athlete)
):
    """Create athlete profile."""
    # Implementation here
    pass


@router.get("/profile", response_model=AthleteProfileResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_athlete)
):
    """Get current athlete's profile."""
    # Implementation here
    pass


@router.put("/profile", response_model=AthleteProfileResponse)
async def update_profile(
    profile_data: AthleteProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_athlete)
):
    """Update athlete profile."""
    # Implementation here
    pass


@router.post("/times", response_model=SwimmingTimeResponse, status_code=status.HTTP_201_CREATED)
async def add_swimming_time(
    time_data: SwimmingTimeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_athlete)
):
    """Add swimming time."""
    # Implementation here
    pass


@router.get("/times", response_model=List[SwimmingTimeResponse])
async def get_swimming_times(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_athlete)
):
    """Get athlete's swimming times."""
    # Implementation here
    pass
