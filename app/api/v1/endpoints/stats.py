"""
Dashboard statistics endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.athlete import AthleteProfile, SwimmingTime
from app.models.recruitment import RecruitmentTracking
from app.models.task import Task
from app.models.document import Document
from pydantic import BaseModel

router = APIRouter()


class DashboardStats(BaseModel):
    """Dashboard statistics response."""
    swimming_times_count: int
    schools_interested_count: int
    tasks_pending_count: int
    documents_count: int


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics for the current athlete.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        Dashboard statistics
    """
    from app.core.exceptions import ForbiddenError

    # Get athlete profile
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        raise ForbiddenError(detail="Athlete profile not found")

    # Count swimming times
    swimming_times_query = select(func.count(SwimmingTime.id)).where(
        SwimmingTime.athlete_id == athlete.id
    )
    swimming_times_result = await db.execute(swimming_times_query)
    swimming_times_count = swimming_times_result.scalar() or 0

    # Count schools interested (recruitment tracking)
    schools_query = select(func.count(RecruitmentTracking.id)).where(
        RecruitmentTracking.athlete_id == athlete.id
    )
    schools_result = await db.execute(schools_query)
    schools_count = schools_result.scalar() or 0

    # Count pending tasks
    tasks_query = select(func.count(Task.id)).where(
        Task.athlete_id == athlete.id,
        Task.status == "pending"
    )
    tasks_result = await db.execute(tasks_query)
    tasks_count = tasks_result.scalar() or 0

    # Count documents
    documents_query = select(func.count(Document.id)).where(
        Document.athlete_id == athlete.id
    )
    documents_result = await db.execute(documents_query)
    documents_count = documents_result.scalar() or 0

    return DashboardStats(
        swimming_times_count=swimming_times_count,
        schools_interested_count=schools_count,
        tasks_pending_count=tasks_count,
        documents_count=documents_count
    )
