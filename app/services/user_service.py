"""
User service for user management operations.
"""
from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError


class UserService:
    """Service for user operations."""

    def __init__(self, db: AsyncSession):
        """
        Initialize user service.

        Args:
            db: Database session
        """
        self.db = db

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User or None if not found
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User or None if not found
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user

        Raises:
            EmailAlreadyExistsError: If email already exists
        """
        # Check if email already exists
        existing_user = await self.get_by_email(user_data.email)
        if existing_user:
            raise EmailAlreadyExistsError()

        # Create new user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Update user.

        Args:
            user_id: User UUID
            user_data: User update data

        Returns:
            Updated user

        Raises:
            UserNotFoundError: If user not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        # Update fields
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user.

        Args:
            email: User email
            password: User password

        Returns:
            User if authenticated, None otherwise
        """
        user = await self.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user
