"""
Tasks endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, alias="status"),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of tasks for the current user.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Filter by task status
        category: Filter by category
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of tasks
    """
    from app.models.athlete import AthleteProfile

    # Get athlete profile for current user
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        return []

    # Build query for tasks
    query = select(Task).where(Task.athlete_id == athlete.id)

    # Apply filters
    if status_filter:
        query = query.where(Task.status == status_filter)
    if category:
        query = query.where(Task.category == category)

    # Apply pagination and ordering
    query = query.order_by(Task.due_date.asc()).offset(skip).limit(limit)

    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get task by ID.

    Args:
        task_id: Task ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Task details
    """
    from uuid import UUID
    from app.core.exceptions import NotFoundError, ForbiddenError
    from app.models.athlete import AthleteProfile

    # Get athlete profile
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        raise ForbiddenError(detail="Athlete profile not found")

    # Get task
    query = select(Task).where(Task.id == UUID(task_id))
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError(detail="Task not found")

    if task.athlete_id != athlete.id:
        raise ForbiddenError(detail="You don't have permission to access this task")

    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task.

    Args:
        task_data: Task data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created task
    """
    from app.core.exceptions import ForbiddenError
    from app.models.athlete import AthleteProfile

    # Get athlete profile
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        raise ForbiddenError(detail="Athlete profile not found")

    # Create task
    task = Task(
        athlete_id=athlete.id,
        **task_data.model_dump()
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task.

    Args:
        task_id: Task ID
        task_data: Task update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated task
    """
    from uuid import UUID
    from app.core.exceptions import NotFoundError, ForbiddenError
    from app.models.athlete import AthleteProfile

    # Get athlete profile
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        raise ForbiddenError(detail="Athlete profile not found")

    # Get task
    query = select(Task).where(Task.id == UUID(task_id))
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError(detail="Task not found")

    if task.athlete_id != athlete.id:
        raise ForbiddenError(detail="You don't have permission to update this task")

    # Update task
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task.

    Args:
        task_id: Task ID
        db: Database session
        current_user: Current authenticated user
    """
    from uuid import UUID
    from app.core.exceptions import NotFoundError, ForbiddenError
    from app.models.athlete import AthleteProfile

    # Get athlete profile
    athlete_query = select(AthleteProfile).where(AthleteProfile.user_id == current_user.id)
    athlete_result = await db.execute(athlete_query)
    athlete = athlete_result.scalar_one_or_none()

    if not athlete:
        raise ForbiddenError(detail="Athlete profile not found")

    # Get task
    query = select(Task).where(Task.id == UUID(task_id))
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundError(detail="Task not found")

    if task.athlete_id != athlete.id:
        raise ForbiddenError(detail="You don't have permission to delete this task")

    # Delete task
    await db.delete(task)
    await db.commit()
