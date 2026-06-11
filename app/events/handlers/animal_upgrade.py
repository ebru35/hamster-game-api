"""Handler for animal_upgrade events."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_animal_upgrade(event: dict) -> None:
    """
    Handle animal_upgrade events.
    
    Logs when a player upgrades an animal.
    Prepare for Discord integration.
    """
    user_email = event.get("user_email")
    payload = event.get("payload", {})
    animal_name = payload.get("animal_name")
    upgrade_level = payload.get("upgrade_level")
    upgrade_cost = payload.get("upgrade_cost")
    
    logger.info(
        f"⬆️ Animal Upgraded | User: {user_email} | "
        f"Animal: {animal_name} | Level: {upgrade_level} | Cost: {upgrade_cost}"
    )
    
    # TODO: Send to Discord webhook
    # TODO: Update stats
