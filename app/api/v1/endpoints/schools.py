"""
Schools endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_db, get_optional_current_user
from app.models.user import User
from app.models.school import School
from app.schemas.school import SchoolResponse

router = APIRouter()


@router.get("/", response_model=List[SchoolResponse])
async def get_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    division: Optional[str] = None,
    state: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get list of schools with optional filters.
    This endpoint is accessible without authentication for browsing.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        division: Filter by division
        state: Filter by state
        db: Database session
        current_user: Optional current authenticated user

    Returns:
        List of schools
    """
    query = select(School)

    # Apply filters
    if division:
        query = query.where(School.division == division)
    if state:
        query = query.where(School.state == state)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    schools = result.scalars().all()

    return schools


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get school by ID.
    This endpoint is accessible without authentication for browsing.

    Args:
        school_id: School ID
        db: Database session
        current_user: Optional current authenticated user

    Returns:
        School details
    """
    from uuid import UUID
    from app.core.exceptions import NotFoundError

    query = select(School).where(School.id == UUID(school_id))
    result = await db.execute(query)
    school = result.scalar_one_or_none()

    if not school:
        raise NotFoundError(detail="School not found")

    return school
