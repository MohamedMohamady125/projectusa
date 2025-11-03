import os
import sys
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get the PORT from environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Log environment info
    logger.info(f"Starting server on port {port}")
    
    # Check for database URL
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        logger.info("DATABASE_URL is configured")
        # Railway uses 'postgresql://' but asyncpg needs 'postgresql+asyncpg://'
        if db_url.startswith("postgresql://"):
            os.environ["DATABASE_URL"] = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            logger.info("Converted DATABASE_URL for asyncpg compatibility")
    else:
        logger.warning("DATABASE_URL not found in environment variables")
    
    # Run the FastAPI app
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
