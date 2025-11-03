"""
Script to create all database tables.
Run this once to initialize your database.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.base import Base

# Import all models to register them with Base
from app.db import *  # noqa


async def create_tables():
    """Create all database tables."""
    print(f"Creating tables in database: {settings.DATABASE_URL.split('@')[1]}")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # Show SQL statements
    )

    async with engine.begin() as conn:
        # Drop all tables (use with caution in production!)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✅ All tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
