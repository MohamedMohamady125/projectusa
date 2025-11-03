"""
Admin-related schemas for dashboard statistics and management.
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class AdminDashboardStats(BaseModel):
    """Admin dashboard statistics."""
    total_users: int
    total_athletes: int
    total_coaches: int
    total_schools: int
    active_users_today: int
    active_users_week: int
    new_users_today: int
    new_users_week: int
    total_swimming_times: int
    total_tasks: int
    pending_verifications: int

    class Config:
        from_attributes = True


class UserListItem(BaseModel):
    """User list item for admin."""
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for admin updating user details."""
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class SchoolListItem(BaseModel):
    """School list item for admin."""
    id: UUID
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    division: Optional[str] = None
    conference: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminActivityLogResponse(BaseModel):
    """Admin activity log response."""
    id: UUID
    admin_id: UUID
    admin_email: str
    action: str
    entity_type: str
    entity_id: Optional[UUID] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: List[BaseModel]
    total: int
    page: int
    page_size: int
    total_pages: int


class UserPaginatedResponse(BaseModel):
    """Paginated user response."""
    items: List[UserListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class SchoolPaginatedResponse(BaseModel):
    """Paginated school response."""
    items: List[SchoolListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminActionRequest(BaseModel):
    """Request for admin actions."""
    reason: Optional[str] = None


class BulkActionRequest(BaseModel):
    """Request for bulk admin actions."""
    ids: List[UUID]
    reason: Optional[str] = None
