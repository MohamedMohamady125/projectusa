"""
Database connection checker for SwimUSA Recruit
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def check_connection():
    """Check database connection."""
    print(f"\n{'='*60}")
    print("Database Connection Checker")
    print(f"{'='*60}\n")

    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Attempting to connect...\n")

    try:
        # Create engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            pool_pre_ping=True
        )

        # Try to connect
        async with engine.begin() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            print(f"\n{'='*60}")
            print("✅ SUCCESS: Database connection successful!")
            print(f"{'='*60}\n")

        await engine.dispose()
        return True

    except Exception as e:
        print(f"\n{'='*60}")
        print("❌ ERROR: Database connection failed!")
        print(f"{'='*60}\n")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}\n")

        print("Common solutions:")
        print("1. Check Supabase project is active at https://supabase.com/dashboard")
        print("2. Verify DATABASE_URL in .env file")
        print("3. Check if password needs to be URL-encoded (! becomes %21)")
        print("4. Ensure Supabase project hasn't been paused/deleted")
        print("5. Try using direct connection instead of pooler\n")

        return False

if __name__ == "__main__":
    asyncio.run(check_connection())
