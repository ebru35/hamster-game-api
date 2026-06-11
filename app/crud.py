"""CRUD operations for events (async version)."""

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Event
from app.schemas import EventRequest
from datetime import datetime


async def create_event(db: AsyncSession, event: EventRequest) -> Event:
    """Create a new event in the database."""
    
    db_event = Event(
        user_email=event.user_email,
        event_name=event.event_name,
        timestamp=event.timestamp,
        click_power=event.payload.click_power,
        coins=event.payload.coins,
        total_clicks=event.payload.total_clicks,
        payload={
            "click_power": event.payload.click_power,
            "coins": event.payload.coins,
            "total_clicks": event.payload.total_clicks,
        },
        processed=False,
        processing=False,
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_unprocessed_events(db: AsyncSession, limit: int = 10) -> list[Event]:
    """Get all unprocessed events that are not currently being processed."""
    stmt = select(Event).where(
        and_(
            Event.processed == False,
            Event.processing == False
        )
    ).order_by(Event.created_at.asc()).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


async def mark_event_processing(db: AsyncSession, event_id: int) -> Event:
    """Mark an event as being processed."""
    stmt = select(Event).where(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if event:
        event.processing = True
        await db.commit()
        await db.refresh(event)
    return event


async def mark_event_processed(db: AsyncSession, event_id: int) -> Event:
    """Mark an event as processed."""
    stmt = select(Event).where(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if event:
        event.processed = True
        event.processing = False
        event.processed_at = datetime.utcnow()
        event.error_message = None
        await db.commit()
        await db.refresh(event)
    return event


async def mark_event_error(db: AsyncSession, event_id: int, error_message: str) -> Event:
    """Mark an event as failed with error message."""
    stmt = select(Event).where(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if event:
        event.processing = False
        event.error_message = error_message
        await db.commit()
        await db.refresh(event)
    return event


async def get_event_by_id(db: AsyncSession, event_id: int) -> Event:
    """Get a specific event by ID."""
    stmt = select(Event).where(Event.id == event_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_events(db: AsyncSession, user_email: str, limit: int = 100) -> list[Event]:
    """Get all events for a specific user."""
    stmt = select(Event).where(
        Event.user_email == user_email
    ).order_by(Event.created_at.desc()).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()
