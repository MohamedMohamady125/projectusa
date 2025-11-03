"""
Database initialization script.
Creates all tables and initializes admin user.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.db.session import async_engine, AsyncSessionLocal
from app.db.base import Base
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from datetime import datetime
from uuid import uuid4


async def init_db():
    """Initialize database."""
    print(f"\n{'='*60}")
    print("Database Initialization")
    print(f"{'='*60}\n")

    print(f"Database URL: {settings.DATABASE_URL}\n")

    try:
        # Create all tables
        print("Creating database tables...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created successfully!\n")

        # Create admin user
        print("Creating admin user...")

        async with AsyncSessionLocal() as session:
            # Check if admin exists
            result = await session.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": settings.ADMIN_EMAIL}
            )
            existing_admin = result.first()

            if existing_admin:
                print(f"ℹ️  Admin user already exists: {settings.ADMIN_EMAIL}\n")
            else:
                # Create admin user
                admin = User(
                    id=uuid4(),
                    email=settings.ADMIN_EMAIL,
                    hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                    first_name=settings.ADMIN_FIRST_NAME,
                    last_name=settings.ADMIN_LAST_NAME,
                    role=UserRole.ADMIN,
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(admin)
                await session.commit()
                print(f"✅ Admin user created successfully!")
                print(f"   Email: {settings.ADMIN_EMAIL}")
                print(f"   Password: {settings.ADMIN_PASSWORD}\n")

        print(f"{'='*60}")
        print("✅ Database initialization completed successfully!")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n{'='*60}")
        print("❌ Database initialization failed!")
        print(f"{'='*60}\n")
        print(f"Error: {str(e)}\n")
        raise


if __name__ == "__main__":
    asyncio.run(init_db())
