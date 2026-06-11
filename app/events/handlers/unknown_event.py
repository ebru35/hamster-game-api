"""Handler for unknown events."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_unknown_event(event: dict) -> None:
    """
    Handle unknown/unregistered events.
    
    Logs but does not crash the application.
    """
    event_name = event.get("event_name", "UNKNOWN")
    user_email = event.get("user_email")
    
    logger.warning(f"⚠️ Unknown event type: {event_name} from {user_email}")
