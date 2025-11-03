"""
Script to create an admin user in the database.
"""
import asyncio
from datetime import datetime
from uuid import uuid4

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin_user():
    """Create an admin user in the database."""
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Admin credentials
        admin_email = "admin@swimusarecruit.com"
        admin_password = "Admin@2024"  # Strong password

        # Hash the password
        hashed_password = pwd_context.hash(admin_password)

        # Create admin user
        admin_user = User(
            id=uuid4(),
            email=admin_email,
            password_hash=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(admin_user)
        await session.commit()

        print("✅ Admin user created successfully!")
        print(f"\n📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print("\n⚠️  Please save these credentials securely!")
        print("You can now login to the admin panel with these credentials.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_admin_user())
