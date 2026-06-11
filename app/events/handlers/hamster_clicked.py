"""Handler for hamster_clicked events."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_hamster_clicked(event: dict) -> None:
    """
    Handle hamster_clicked events.
    
    Logs user activity and click statistics.
    Prepare for Discord integration.
    """
    user_email = event.get("user_email")
    click_power = event.get("click_power")
    total_clicks = event.get("total_clicks")
    coins = event.get("coins")
    
    logger.info(
        f"🐹 Hamster Clicked | User: {user_email} | "
        f"Power: {click_power} | Total Clicks: {total_clicks} | Coins: {coins}"
    )
    
    from app.notifications import send_discord_message

    message = (
        f"🐹 Hamster Clicked\n"
        f"User: {user_email}\n"
        f"Power: {click_power}\n"
        f"Total Clicks: {total_clicks}\n"
        f"Coins: {coins}"
    )
    
    await send_discord_message(message)
