"""Script to create database tables."""

import asyncio
import logging
from sqlalchemy import text
from app.database import engine, Base
from app.models import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    """Create all database tables and add missing columns if needed."""
    try:
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                text(
                    """
                    ALTER TABLE events
                    ADD COLUMN IF NOT EXISTS processing BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS error_message TEXT
                    """
                )
            )
        logger.info("✓ Database tables created and schema verified successfully!")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to create tables: {str(e)}")
        logger.error("Make sure your DATABASE_URL is correct:")
        logger.error("  Format: postgresql://user:password@host/database?sslmode=require")
        logger.error("  Get it from: https://console.neon.tech")
        return False


if __name__ == "__main__":
    import sys
    success = asyncio.run(create_tables())
    sys.exit(0 if success else 1)

