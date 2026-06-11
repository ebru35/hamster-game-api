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
    
    from app.notifications import send_discord_message

    message = (
        f"⬆️ Animal Upgraded\n"
        f"User: {user_email}\n"
        f"Animal: {animal_name}\n"
        f"Level: {upgrade_level}\n"
        f"Cost: {upgrade_cost}"
    )
    
    await send_discord_message(message)
