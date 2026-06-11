"""Test script for event dispatcher and handlers - tests without needing the API."""

import asyncio
import logging
from app.events.dispatcher import dispatch_event

# Configure logging to see handler output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def test_event_system():
    """Test the event dispatcher and all handlers."""
    print("🧪 Testing Event Dispatcher and Handlers\n")
    
    # Test 1: Hamster clicked
    print("📌 Test 1: Hamster Clicked Event")
    event1 = {
        "id": 1,
        "user_email": "player1@example.com",
        "event_name": "hamster_clicked",
        "click_power": 5,
        "coins": 250,
        "total_clicks": 1000,
        "payload": {"click_power": 5, "coins": 250, "total_clicks": 1000},
    }
    await dispatch_event(event1)
    
    # Test 2: Animal unlocked
    print("\n📌 Test 2: Animal Unlocked Event")
    event2 = {
        "id": 2,
        "user_email": "player2@example.com",
        "event_name": "animal_unlock",
        "click_power": None,
        "coins": None,
        "total_clicks": None,
        "payload": {
            "animal_name": "Rabbit",
            "animal_type": "speed_booster",
        },
    }
    await dispatch_event(event2)
    
    # Test 3: Animal upgraded
    print("\n📌 Test 3: Animal Upgraded Event")
    event3 = {
        "id": 3,
        "user_email": "player3@example.com",
        "event_name": "animal_upgrade",
        "click_power": None,
        "coins": None,
        "total_clicks": None,
        "payload": {
            "animal_name": "Hamster",
            "upgrade_level": 2,
            "upgrade_cost": 500,
        },
    }
    await dispatch_event(event3)
    
    # Test 4: Game ended
    print("\n📌 Test 4: Game Ended Event")
    event4 = {
        "id": 4,
        "user_email": "player4@example.com",
        "event_name": "game_end",
        "click_power": None,
        "coins": None,
        "total_clicks": None,
        "payload": {
            "final_score": 10000,
            "total_clicks": 5000,
            "total_coins": 2500,
            "playtime_seconds": 600,
        },
    }
    await dispatch_event(event4)
    
    # Test 5: Unknown event
    print("\n📌 Test 5: Unknown Event")
    event5 = {
        "id": 5,
        "user_email": "player5@example.com",
        "event_name": "unknown_event_type",
        "click_power": None,
        "coins": None,
        "total_clicks": None,
        "payload": {},
    }
    await dispatch_event(event5)
    
    print("\n✨ All handler tests completed!")


if __name__ == "__main__":
    asyncio.run(test_event_system())
