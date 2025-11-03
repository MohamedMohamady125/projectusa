"""
FastAPI dependencies for authentication and authorization.
"""
from typing import Optional
from uuid import UUID
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_token
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InactiveUserError,
    UnverifiedUserError
)
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.services.user_service import UserService

# HTTP Bearer token authentication
security = HTTPBearer()


async def get_db():
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        AuthenticationError: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise AuthenticationError(detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationError(detail="Invalid token payload")

    user_service = UserService(db)
    user = await user_service.get_by_id(UUID(user_id))

    if not user:
        raise AuthenticationError(detail="User not found")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current active user

    Raises:
        InactiveUserError: If user is not active
    """
    if not current_user.is_active:
        raise InactiveUserError()

    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency to get the current verified user.

    Args:
        current_user: Current active user

    Returns:
        User: Current verified user

    Raises:
        UnverifiedUserError: If user email is not verified
    """
    if not current_user.is_verified:
        raise UnverifiedUserError()

    return current_user


async def get_current_athlete(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Dependency to ensure current user is an athlete.

    Args:
        current_user: Current verified user

    Returns:
        User: Current athlete user

    Raises:
        AuthorizationError: If user is not an athlete
    """
    if current_user.role != UserRole.ATHLETE:
        raise AuthorizationError(detail="Only athletes can access this resource")

    return current_user


async def get_current_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency to ensure current user is an admin.

    Args:
        current_user: Current active user

    Returns:
        User: Current admin user

    Raises:
        AuthorizationError: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError(detail="Admin access required")

    return current_user


async def get_current_coach(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Dependency to ensure current user is a coach.

    Args:
        current_user: Current verified user

    Returns:
        User: Current coach user

    Raises:
        AuthorizationError: If user is not a coach
    """
    if current_user.role != UserRole.COACH:
        raise AuthorizationError(detail="Only coaches can access this resource")

    return current_user


async def get_current_parent(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Dependency to ensure current user is a parent.

    Args:
        current_user: Current verified user

    Returns:
        User: Current parent user

    Raises:
        AuthorizationError: If user is not a parent
    """
    if current_user.role != UserRole.PARENT:
        raise AuthorizationError(detail="Only parents can access this resource")

    return current_user


def check_admin_or_self(current_user: User, target_user_id: UUID) -> bool:
    """
    Check if current user is admin or accessing their own resources.

    Args:
        current_user: Current authenticated user
        target_user_id: ID of the user being accessed

    Returns:
        bool: True if authorized

    Raises:
        AuthorizationError: If user is not authorized
    """
    if current_user.role == UserRole.ADMIN or current_user.id == target_user_id:
        return True
    raise AuthorizationError(detail="Not authorized to access this resource")


async def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get the current user.
    Returns None if no valid token is provided.

    Args:
        authorization: Optional authorization header
        db: Database session

    Returns:
        Optional[User]: Current user or None
    """
    if not authorization:
        return None

    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None

        payload = verify_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user_service = UserService(db)
        user = await user_service.get_by_id(UUID(user_id))

        return user if user and user.is_active else None
    except Exception:
        return None


class Pagination:
    """Pagination dependency."""

    def __init__(
        self,
        skip: int = 0,
        limit: int = settings.DEFAULT_PAGE_SIZE
    ):
        """
        Initialize pagination parameters.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
        """
        self.skip = max(0, skip)
        self.limit = min(limit, settings.MAX_PAGE_SIZE)
