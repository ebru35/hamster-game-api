"""Notification utilities for external integrations like Discord."""

import logging
from typing import Optional
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def send_discord_message(content: str) -> None:
    """Send a message to the configured Discord webhook."""
    discord_url: Optional[str] = settings.discord_webhook_url
    if not discord_url:
        logger.debug("Discord webhook URL not configured, skipping Discord notification.")
        return

    payload = {"content": content}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(discord_url, json=payload)
            if response.status_code >= 400:
                logger.warning(
                    f"Discord notification failed: {response.status_code} - {response.text}"
                )
            else:
                logger.info("Discord notification sent successfully.")
    except Exception as exc:
        logger.error(f"Error sending Discord notification: {exc}", exc_info=True)
