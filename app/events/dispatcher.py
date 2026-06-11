"""Event dispatcher - routes events to appropriate handlers."""

import logging
from app.events.handlers.hamster_clicked import handle_hamster_clicked
from app.events.handlers.animal_unlock import handle_animal_unlock
from app.events.handlers.animal_upgrade import handle_animal_upgrade
from app.events.handlers.game_end import handle_game_end
from app.events.handlers.unknown_event import handle_unknown_event

logger = logging.getLogger(__name__)


async def dispatch_event(event: dict) -> None:
    """
    Dispatch an event to the appropriate handler based on event_name.
    
    Args:
        event: Dictionary containing event data
    """
    event_name = event.get("event_name")
    
    try:
        if event_name == "hamster_clicked":
            await handle_hamster_clicked(event)
        elif event_name == "animal_unlock":
            await handle_animal_unlock(event)
        elif event_name == "animal_upgrade":
            await handle_animal_upgrade(event)
        elif event_name == "game_end":
            await handle_game_end(event)
        else:
            await handle_unknown_event(event)
    except Exception as e:
        logger.error(f"Error dispatching event {event_name}: {str(e)}", exc_info=True)
        # Don't crash, just log the error
        raise  # Re-raise so event loop can catch and handle it
