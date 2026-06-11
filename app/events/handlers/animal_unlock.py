"""Handler for animal_unlock events."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_animal_unlock(event: dict) -> None:
    """
    Handle animal_unlock events.
    
    Logs when a player unlocks a new animal.
    Prepare for Discord integration.
    """
    user_email = event.get("user_email")
    payload = event.get("payload", {})
    animal_name = payload.get("animal_name")
    animal_type = payload.get("animal_type")
    
    logger.info(
        f"🦁 Animal Unlocked | User: {user_email} | "
        f"Animal: {animal_name} | Type: {animal_type}"
    )
    
    # TODO: Send to Discord webhook
    # TODO: Update player profile
