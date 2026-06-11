"""Event processing loop - async worker that processes unprocessed events."""

import asyncio
import logging
from app.database import async_session
from app.events.dispatcher import dispatch_event
import app.crud as crud

logger = logging.getLogger(__name__)


async def process_events():
    """
    Main event processing loop.
    
    Continuously checks for unprocessed events and dispatches them to handlers.
    Features:
    - Prevents duplicate processing with processing flag
    - Captures and logs errors without crashing
    - Sleeps 5 seconds between checks
    """
    logger.info("🚀 Event processing loop started")
    
    while True:
        try:
            async with async_session() as db:
                # Get unprocessed events (not currently being processed)
                events = await crud.get_unprocessed_events(db, limit=10)
                
                if events:
                    logger.info(f"📋 Found {len(events)} unprocessed events")
                    
                    for event in events:
                        try:
                            # Mark as processing to prevent duplicate handling
                            await crud.mark_event_processing(db, event.id)
                            logger.info(f"⚙️  Processing event {event.id} ({event.event_name})")
                            
                            # Convert event to dict for dispatcher
                            event_dict = {
                                "id": event.id,
                                "user_email": event.user_email,
                                "event_name": event.event_name,
                                "timestamp": event.timestamp,
                                "click_power": event.click_power,
                                "coins": event.coins,
                                "total_clicks": event.total_clicks,
                                "payload": event.payload,
                            }
                            
                            # Dispatch to appropriate handler
                            await dispatch_event(event_dict)
                            
                            # Mark as processed
                            await crud.mark_event_processed(db, event.id)
                            logger.info(f"✅ Event {event.id} processed successfully")
                            
                        except Exception as e:
                            # Log error but don't crash the loop
                            error_msg = f"{type(e).__name__}: {str(e)}"
                            logger.error(
                                f"❌ Error processing event {event.id}: {error_msg}",
                                exc_info=True
                            )
                            
                            # Mark event with error, reset processing flag
                            await crud.mark_event_error(db, event.id, error_msg)
                else:
                    logger.debug("No unprocessed events found")
                
                # Sleep before next check
                await asyncio.sleep(5)
                
        except Exception as e:
            logger.error(f"💥 Critical error in event loop: {str(e)}", exc_info=True)
            # Sleep before retrying
            await asyncio.sleep(5)


def run_event_loop():
    """Run the async event loop (for use with asyncio.run)."""
    asyncio.run(process_events())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_event_loop()
