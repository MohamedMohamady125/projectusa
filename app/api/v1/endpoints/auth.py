"""
Authentication endpoints for user registration, login, and password management.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_db, get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_verification_token,
    verify_verification_token
)
from app.core.exceptions import InvalidCredentialsError, InvalidTokenError
from app.models.user import User
from app.schemas.base import MessageResponse, TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse, EmailVerification
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user

    Raises:
        EmailAlreadyExistsError: If email already exists
    """
    user_service = UserService(db)
    user = await user_service.create(user_data)

    # Generate verification token
    verification_token = create_verification_token(user.email)
    user.verification_token = verification_token
    await db.commit()

    # TODO: Send verification email
    # await email_service.send_verification_email(user.email, verification_token)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login user and return access tokens.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        Access and refresh tokens

    Raises:
        InvalidCredentialsError: If credentials are invalid
    """
    user_service = UserService(db)
    user = await user_service.authenticate(credentials.email, credentials.password)

    if not user:
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InvalidCredentialsError(detail="Account is inactive")

    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    verification_data: EmailVerification,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify user email address.

    Args:
        verification_data: Email verification data
        db: Database session

    Returns:
        Success message

    Raises:
        InvalidTokenError: If token is invalid
    """
    email = verify_verification_token(verification_data.token)
    if not email:
        raise InvalidTokenError()

    user_service = UserService(db)
    user = await user_service.get_by_email(email)
    if not user:
        raise InvalidTokenError()

    user.is_verified = True
    user.verification_token = None
    await db.commit()

    return MessageResponse(
        message="Email verified successfully",
        detail="Your email has been verified. You can now access all features."
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user.

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    # In a production environment, you would invalidate the token here
    # For example, by adding it to a blacklist in Redis
    return MessageResponse(
        message="Logged out successfully",
        detail="Your session has been terminated."
    )
