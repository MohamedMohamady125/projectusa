"""
User management endpoints.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user, get_current_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Get list of all users (Admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of users
    """
    user_service = UserService(db)
    users = await user_service.list(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.

    Args:
        user_id: User UUID
        db: Database session
        current_user: Current authenticated user

    Returns:
        User information
    """
    user_service = UserService(db)
    user = await user_service.get(user_id)

    # Users can only view their own profile unless they are admin
    if user.id != current_user.id and current_user.role != "admin":
        from app.core.exceptions import ForbiddenError
        raise ForbiddenError("You can only view your own profile")

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user information.

    Args:
        user_id: User UUID
        user_update: User update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Updated user information
    """
    # Users can only update their own profile unless they are admin
    if user_id != current_user.id and current_user.role != "admin":
        from app.core.exceptions import ForbiddenError
        raise ForbiddenError("You can only update your own profile")

    user_service = UserService(db)
    user = await user_service.update(user_id, user_update)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Delete user (Admin only).

    Args:
        user_id: User UUID
        db: Database session
    """
    user_service = UserService(db)
    await user_service.delete(user_id)
