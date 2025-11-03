"""
Admin endpoints for user management, statistics, and system administration.
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_admin
from app.core.exceptions import NotFoundError
from app.models.user import User, UserRole
from app.schemas.admin import (
    AdminDashboardStats,
    UserListItem,
    UserUpdate,
    UserPaginatedResponse,
    SchoolListItem,
    SchoolPaginatedResponse,
    AdminActivityLogResponse,
    AdminActionRequest
)
from app.schemas.base import MessageResponse
from app.schemas.user import UserResponse
from app.schemas.school import SchoolResponse, SchoolCreate
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/dashboard/stats", response_model=AdminDashboardStats)
async def get_admin_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get dashboard statistics for admin panel.

    Requires admin role.
    """
    admin_service = AdminService(db)
    return await admin_service.get_dashboard_stats()


@router.get("/users", response_model=UserPaginatedResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get paginated list of users with optional filters.

    Filters:
    - role: Filter by user role
    - search: Search by email
    - is_active: Filter by active status
    - is_verified: Filter by verification status

    Requires admin role.
    """
    admin_service = AdminService(db)
    users, total = await admin_service.get_users_paginated(
        skip=skip,
        limit=limit,
        role=role,
        search=search,
        is_active=is_active,
        is_verified=is_verified
    )

    total_pages = (total + limit - 1) // limit
    page = (skip // limit) + 1

    return UserPaginatedResponse(
        items=[UserListItem.model_validate(user) for user in users],
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_details(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get detailed information about a specific user.

    Requires admin role.
    """
    admin_service = AdminService(db)
    user = await admin_service.get_user_by_id(user_id)

    if not user:
        raise NotFoundError(detail="User not found")

    return user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Update user details.

    Can update:
    - email
    - role
    - is_active
    - is_verified

    Requires admin role.
    """
    admin_service = AdminService(db)
    user = await admin_service.update_user(user_id, user_update, current_admin)

    if not user:
        raise NotFoundError(detail="User not found")

    return user


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete a user.

    Requires admin role.
    """
    admin_service = AdminService(db)
    success = await admin_service.delete_user(user_id, current_admin)

    if not success:
        raise NotFoundError(detail="User not found")

    return MessageResponse(
        message="User deleted successfully",
        detail=f"User with ID {user_id} has been removed from the system"
    )


@router.post("/users/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Activate a user account.

    Requires admin role.
    """
    admin_service = AdminService(db)
    user_update = UserUpdate(is_active=True)
    user = await admin_service.update_user(user_id, user_update, current_admin)

    if not user:
        raise NotFoundError(detail="User not found")

    return user


@router.post("/users/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Deactivate a user account.

    Requires admin role.
    """
    admin_service = AdminService(db)
    user_update = UserUpdate(is_active=False)
    user = await admin_service.update_user(user_id, user_update, current_admin)

    if not user:
        raise NotFoundError(detail="User not found")

    return user


@router.post("/users/{user_id}/verify", response_model=UserResponse)
async def verify_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Manually verify a user's email.

    Requires admin role.
    """
    admin_service = AdminService(db)
    user_update = UserUpdate(is_verified=True)
    user = await admin_service.update_user(user_id, user_update, current_admin)

    if not user:
        raise NotFoundError(detail="User not found")

    return user


@router.get("/schools", response_model=SchoolPaginatedResponse)
async def list_schools(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    state: Optional[str] = None,
    division: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get paginated list of schools with optional filters.

    Filters:
    - search: Search by name or city
    - state: Filter by state
    - division: Filter by NCAA division
    - is_active: Filter by active status

    Requires admin role.
    """
    admin_service = AdminService(db)
    schools, total = await admin_service.get_schools_paginated(
        skip=skip,
        limit=limit,
        search=search,
        state=state,
        division=division,
        is_active=is_active
    )

    total_pages = (total + limit - 1) // limit
    page = (skip // limit) + 1

    return SchoolPaginatedResponse(
        items=[SchoolListItem.model_validate(school) for school in schools],
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.post("/schools", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Create a new school.

    Requires admin role.
    """
    admin_service = AdminService(db)
    school = await admin_service.create_school(school_data, current_admin)
    return school


@router.post("/schools/{school_id}/toggle-active", response_model=SchoolResponse)
async def toggle_school_active(
    school_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Toggle school active status.

    Requires admin role.
    """
    admin_service = AdminService(db)
    school = await admin_service.toggle_school_active(school_id, current_admin)

    if not school:
        raise NotFoundError(detail="School not found")

    return school


@router.get("/activity-logs")
async def get_activity_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    admin_id: Optional[UUID] = None,
    action: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Get admin activity logs.

    Filters:
    - admin_id: Filter by admin user
    - action: Filter by action type

    Requires admin role.
    """
    admin_service = AdminService(db)
    logs, total = await admin_service.get_activity_logs(
        skip=skip,
        limit=limit,
        admin_id=admin_id,
        action=action
    )

    total_pages = (total + limit - 1) // limit
    page = (skip // limit) + 1

    # Convert logs to response format
    log_responses = []
    for log in logs:
        log_responses.append(AdminActivityLogResponse(
            id=log.id,
            admin_id=log.admin_id,
            admin_email=log.admin.email,
            action=log.action,
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            details=log.details,
            ip_address=log.ip_address,
            created_at=log.created_at
        ))

    return {
        "items": log_responses,
        "total": total,
        "page": page,
        "page_size": limit,
        "total_pages": total_pages
    }
