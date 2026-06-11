"""Test script for webhook endpoints - sends sample events to local API."""

import httpx
import asyncio
import json
from datetime import datetime
from typing import Optional

# Configuration
API_URL = "http://localhost:8000"
WEBHOOK_SECRET = None  # Set to your WEBHOOK_SECRET if configured


async def send_event(
    event_name: str,
    user_email: str = "player@example.com",
    click_power: Optional[int] = None,
    coins: Optional[int] = None,
    total_clicks: Optional[int] = None,
    payload: Optional[dict] = None,
):
    """Send an event to the API."""
    
    request_body = {
        "user_email": user_email,
        "event_name": event_name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload or {
            "click_power": click_power or 1,
            "coins": coins or 100,
            "total_clicks": total_clicks or 50,
        }
    }
    
    headers = {}
    if WEBHOOK_SECRET:
        headers["X-Webhook-Secret"] = WEBHOOK_SECRET
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_URL}/events",
                json=request_body,
                headers=headers,
                timeout=5.0
            )
            print(f"✅ {event_name}: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ {event_name}: {str(e)}")


async def test_webhook():
    """Run all webhook tests."""
    print("🧪 Testing Hamster Game API Webhook\n")
    
    # Test 1: Hamster clicked
    print("📌 Test 1: Hamster Clicked")
    await send_event(
        event_name="hamster_clicked",
        user_email="player1@example.com",
        click_power=5,
        coins=250,
        total_clicks=1000
    )
    
    # Test 2: Animal unlocked
    print("\n📌 Test 2: Animal Unlocked")
    await send_event(
        event_name="animal_unlock",
        user_email="player2@example.com",
        payload={
            "animal_name": "Rabbit",
            "animal_type": "speed_booster",
        }
    )
    
    # Test 3: Animal upgraded
    print("\n📌 Test 3: Animal Upgraded")
    await send_event(
        event_name="animal_upgrade",
        user_email="player3@example.com",
        payload={
            "animal_name": "Hamster",
            "upgrade_level": 2,
            "upgrade_cost": 500,
        }
    )
    
    # Test 4: Game ended
    print("\n📌 Test 4: Game Ended")
    await send_event(
        event_name="game_end",
        user_email="player4@example.com",
        payload={
            "final_score": 10000,
            "total_clicks": 5000,
            "total_coins": 2500,
            "playtime_seconds": 600,
        }
    )
    
    # Test 5: Health check
    print("\n📌 Test 5: Health Check")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/health", timeout=5.0)
            print(f"✅ Health: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Health: {str(e)}")
    
    print("\n✨ Tests completed!")


if __name__ == "__main__":
    print("Make sure the API is running: python -m uvicorn app.main:app --reload\n")
    asyncio.run(test_webhook())
