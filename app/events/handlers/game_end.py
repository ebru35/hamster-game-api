"""Handler for game_end events."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def handle_game_end(event: dict) -> None:
    """
    Handle game_end events.
    
    Logs game completion and final statistics.
    Prepare for Discord integration.
    """
    user_email = event.get("user_email")
    payload = event.get("payload", {})
    final_score = payload.get("final_score")
    total_clicks = payload.get("total_clicks")
    total_coins = payload.get("total_coins")
    playtime_seconds = payload.get("playtime_seconds")
    
    logger.info(
        f"🏁 Game Ended | User: {user_email} | "
        f"Score: {final_score} | Clicks: {total_clicks} | Coins: {total_coins} | "
        f"Time: {playtime_seconds}s"
    )
    
    from app.notifications import send_discord_message

    message = (
        f"🏁 Game Ended\n"
        f"User: {user_email}\n"
        f"Score: {final_score}\n"
        f"Clicks: {total_clicks}\n"
        f"Coins: {total_coins}\n"
        f"Playtime: {playtime_seconds}s"
    )
    
    await send_discord_message(message)
