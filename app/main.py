"""FastAPI application for hamster game events."""

from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import Optional

from app.config import get_settings
from app.database import get_db, init_db
from app.schemas import EventRequest, EventResponse
import app.crud as crud

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app first (before DB operations)
app = FastAPI(
    title="Hamster Game API",
    description="API for hamster clicking game events",
    version="1.0.0",
)

settings = get_settings()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        await init_db()
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.warning(f"Could not create database tables on startup: {str(e)}")
        logger.warning("Make sure DATABASE_URL is configured correctly in .env")
        logger.warning("Run: python create_tables.py to create tables manually")


def verify_webhook_secret(x_webhook_secret: Optional[str] = Header(None)) -> bool:
    """Verify webhook secret from X-Webhook-Secret header."""
    # If no secret is configured, allow all requests
    if not settings.webhook_secret:
        return True
    
    # If secret is configured, require and verify it
    if not x_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Webhook-Secret header"
        )
    
    if x_webhook_secret != settings.webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Webhook-Secret"
        )
    
    return True


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/events", response_model=EventResponse, tags=["Events"])
async def receive_event(
    event: EventRequest,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_webhook_secret)
):
    """
    Receive a game event and store in database.
    
    Optional header: X-Webhook-Secret (required if WEBHOOK_SECRET env var is set)
    
    Expected request body:
    ```json
    {
      "user_email": "player@example.com",
      "event_name": "hamster_clicked",
      "timestamp": "2026-06-11T12:00:00Z",
      "payload": {
        "click_power": 1,
        "coins": 100,
        "total_clicks": 50
      }
    }
    ```
    """
    try:
        db_event = await crud.create_event(db=db, event=event)
        logger.info(
            f"Event stored | ID: {db_event.id} | "
            f"User: {db_event.user_email} | Event: {db_event.event_name}"
        )
        return EventResponse(status="success", event_id=db_event.id)
    except Exception as e:
        logger.error(f"Error storing event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store event"
        )


@app.post("/66845e3b-feb9-40f1-bc83-d91eca5aea13", response_model=EventResponse, tags=["Events"])
async def receive_event_legacy(
    event: EventRequest,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_webhook_secret)
):
    """
    Legacy n8n-compatible endpoint.
    
    Same as POST /events but uses the old n8n webhook path for backward compatibility.
    """
    return await receive_event(event, db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )

