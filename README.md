# Hamster Game API

FastAPI application for storing hamster clicking game events in PostgreSQL. Replaces n8n webhook workflow.

## Features

- 🚀 **FastAPI** with async/await for high performance
- 💾 **PostgreSQL (Neon)** for persistent storage
- ⚙️ **Async event processing** with dispatcher and handlers
- 🔐 **Webhook secret validation** with optional header authentication
- 📝 **Clean, simple code** suitable for school projects
- 🔄 **Backward compatible** with old n8n webhook path
- 🧪 **Complete test scripts** for development

## Project Structure

```
hamster-game-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration (environment variables)
│   ├── database.py          # Async database setup
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Async database operations
│   └── events/
│       ├── dispatcher.py     # Event routing to handlers
│       └── handlers/         # Event handlers (5 types)
│           ├── hamster_clicked.py
│           ├── animal_unlock.py
│           ├── animal_upgrade.py
│           ├── game_end.py
│           └── unknown_event.py
├── event_loop.py            # Background async event processor
├── create_tables.py         # Database table creation utility
├── test_webhook.py          # Test webhook endpoints
├── test_event_system.py     # Test handlers without API
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── README.md
└── .gitignore
```

## Database Schema

Events table with fields:
- `id` (Primary Key)
- `user_email` (indexed)
- `event_name` (indexed)
- `timestamp` (timezone-aware)
- `click_power`, `coins`, `total_clicks` (optional)
- `payload` (JSONB for flexible data)
- `processed` (Boolean, indexed - false = unprocessed)
- `processing` (Boolean, indexed - true = currently being processed)
- `error_message` (Text - error details if processing failed)
- `created_at`, `processed_at` (timestamps)

## Setup

### 1. Prerequisites

- Python 3.11+ (3.12 recommended)
- PostgreSQL database (Neon: https://neon.tech)
- Git

### 2. Clone and Install

```bash
git clone https://github.com/ebru35/hamster-game-api.git
cd hamster-game-api

pip install -r requirements.txt
```

### 3. Configure Database - IMPORTANT!

1. **Get your Neon connection string:**
   - Go to https://console.neon.tech
   - Select your project
   - Click "Connection string" (top right)
   - Copy the PostgreSQL URL
   - Keep it safe - this is sensitive data!

2. **Create and update `.env` file:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your actual password
   ```
   
   Your `.env` should look like:
   ```env
   DATABASE_URL=postgresql://neondb_owner:YOUR_PASSWORD@ep-xxxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   API_HOST=0.0.0.0
   API_PORT=8000
   DEBUG=False
   WEBHOOK_SECRET=optional_secret_key_for_auth
   ```

3. **Create database tables:**
   ```bash
   python create_tables.py
   ```
   
   Expected output:
   ```
   INFO:root:Creating database tables...
   INFO:root:✓ Database tables created successfully!
   ```

### 4. Run Locally

**Terminal 1 - Start API Server:**
```bash
uvicorn app.main:app --reload
```

- API runs at: http://localhost:8000
- Docs at: http://localhost:8000/docs
- ReDoc at: http://localhost:8000/redoc

**Terminal 2 - Start Event Processing Loop:**
```bash
python event_loop.py
```

This runs the async event loop that:
- Checks for unprocessed events every 5 seconds
- Sets `processing = true` to prevent duplicate handling
- Dispatches to appropriate handler
- Catches errors and stores in `error_message`
- Sets `processing = false` if error occurs
- Marks as `processed = true` on success

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{"status": "ok"}
```

### Receive Event - Main Endpoint
```
POST /events
Content-Type: application/json
X-Webhook-Secret: your_secret_here (optional if WEBHOOK_SECRET env var set)
```

Request body:
```json
{
  "user_email": "player@example.com",
  "event_name": "hamster_clicked",
  "timestamp": "2026-06-11T12:00:00Z",
  "payload": {
    "click_power": 1,
    "coins": 100,
    "total_clicks": 50
  }
}
```

Response:
```json
{
  "status": "success",
  "event_id": 1
}
```

### Legacy n8n Endpoint
```
POST /66845e3b-feb9-40f1-bc83-d91eca5aea13
```

Same format as `/events`. Use for backward compatibility.

## Event Types

The API supports these event types with dedicated handlers:

### 1. `hamster_clicked`
When player clicks the hamster.

Handler logs: User email, coins, total_clicks, click_power

```json
{
  "event_name": "hamster_clicked",
  "user_email": "player@example.com",
  "payload": {
    "click_power": 1,
    "coins": 100,
    "total_clicks": 50
  }
}
```

### 2. `animal_unlock`
When player unlocks a new animal.

Handler logs: Animal name and type

```json
{
  "event_name": "animal_unlock",
  "user_email": "player@example.com",
  "payload": {
    "animal_name": "Rabbit",
    "animal_type": "speed_booster"
  }
}
```

### 3. `animal_upgrade`
When player upgrades an animal.

Handler logs: Animal name, upgrade level, cost

```json
{
  "event_name": "animal_upgrade",
  "user_email": "player@example.com",
  "payload": {
    "animal_name": "Hamster",
    "upgrade_level": 2,
    "upgrade_cost": 500
  }
}
```

### 4. `game_end`
When player finishes playing.

Handler logs: Final score, total clicks, coins, playtime

```json
{
  "event_name": "game_end",
  "user_email": "player@example.com",
  "payload": {
    "final_score": 10000,
    "total_clicks": 5000,
    "total_coins": 2500,
    "playtime_seconds": 600
  }
}
```

### 5. Unknown Events
Any other event type is logged as unknown. The app does NOT crash.

## Webhook Secret Authentication

### Optional Configuration

If you want to secure your webhook endpoints:

1. **Generate a secret:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Add to `.env`:**
   ```env
   WEBHOOK_SECRET=your_generated_secret_here
   ```

3. **Send with requests:**
   ```bash
   curl -X POST http://localhost:8000/events \
     -H "Content-Type: application/json" \
     -H "X-Webhook-Secret: your_generated_secret_here" \
     -d '{...event data...}'
   ```

If `WEBHOOK_SECRET` is not set or empty, all requests are allowed (no authentication required).

## Testing

### Test the Webhook Endpoints

```bash
python test_webhook.py
```

This sends 5 sample events to your local API:
1. Hamster clicked
2. Animal unlocked
3. Animal upgraded
4. Game ended
5. Health check

### Test Handlers Without API

```bash
python test_event_system.py
```

This tests the dispatcher and handlers directly without needing the API running.

### Manual Testing with curl

```bash
# Send hamster_clicked event
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "player@example.com",
    "event_name": "hamster_clicked",
    "timestamp": "2026-06-11T12:00:00Z",
    "payload": {
      "click_power": 5,
      "coins": 250,
      "total_clicks": 1000
    }
  }'

# Check health
curl http://localhost:8000/health
```

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Event Processing Flow

```
1. Game sends POST /events
   ↓
2. API receives and validates with Pydantic
   ↓
3. Event stored in database (processed=false, processing=false)
   ↓
4. API responds with event_id
   ↓
5. Event loop polls every 5 seconds
   ↓
6. Finds unprocessed events (processed=false AND processing=false)
   ↓
7. Sets processing=true (prevents duplicate handling)
   ↓
8. Dispatcher routes to handler based on event_name
   ↓
9. Handler processes (logs, Discord, etc)
   ↓
10a. SUCCESS: Sets processed=true, processing=false
10b. ERROR: Stores error_message, processing=false
```

## Creating Custom Event Handlers

### Example: Add a new event type

1. **Create handler file** `app/events/handlers/my_handler.py`:

```python
import logging

logger = logging.getLogger(__name__)

async def handle_my_event(event: dict) -> None:
    """Handle custom event type."""
    user_email = event.get("user_email")
    logger.info(f"Custom event from {user_email}")
```

2. **Update dispatcher** in `app/events/dispatcher.py`:

```python
from app.events.handlers.my_handler import handle_my_event

async def dispatch_event(event: dict) -> None:
    event_name = event.get("event_name")
    
    try:
        if event_name == "hamster_clicked":
            await handle_hamster_clicked(event)
        elif event_name == "my_event":
            await handle_my_event(event)
        # ... other handlers
        else:
            await handle_unknown_event(event)
    except Exception as e:
        logger.error(f"Error dispatching: {str(e)}", exc_info=True)
        raise
```

3. **Send events:**

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "player@example.com",
    "event_name": "my_event",
    "timestamp": "2026-06-11T12:00:00Z",
    "payload": {"key": "value"}
  }'
```

## Deployment

### Docker

```bash
# Build
docker build -t hamster-game-api .

# Run with API on port 8000
docker run -p 8000:8000 --env-file .env hamster-game-api uvicorn app.main:app --host 0.0.0.0

# Run event loop in another container
docker run --env-file .env hamster-game-api python event_loop.py
```

### Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string

Optional:
- `WEBHOOK_SECRET` - For authentication (defaults to allow all requests)
- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: False)

## Troubleshooting

### Database Connection Error

**Error:** `could not translate host name "ep-xxxx" to address`

**Solution:**
1. Check `.env` DATABASE_URL is correct
2. Verify password is correct (special characters need escaping)
3. Check internet connection to Neon
4. Restart the application

### Port Already in Use

**Error:** `Address already in use: 0.0.0.0:8000`

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

### Events Not Processing

**Debug:**
1. Check event loop is running in Terminal 2
2. Check database has events with `processed=false`
3. Look for errors in event loop output
4. Check error_message field in database

## Technologies

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - ORM with async support
- **asyncpg** - Async PostgreSQL driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **PostgreSQL** - Database

## License

MIT

## Notes for School Project

This project is intentionally kept simple and educational:
- Clear function names and comments
- Simple event handling pattern
- No complex frameworks or patterns
- Easy to understand and modify
- Good starter for learning:
  - Async/await in Python
  - Web APIs with FastAPI
  - Database with SQLAlchemy
  - Event processing patterns

### Railway, Render, or Vercel

1. Push to GitHub
2. Connect repository to deployment platform
3. Set `DATABASE_URL` environment variable
4. Deploy!

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong database passwords
- [ ] Enable SSL/TLS for database connections
- [ ] Monitor logs regularly
- [ ] Set up database backups
- [ ] Use environment variables, not hardcoded values
- [ ] Run behind a reverse proxy (nginx, etc)

## Troubleshooting

### Password Authentication Failed?

**Error:** `password authentication failed for user 'neondb_owner'`

**Solution:**
1. Check your `.env` file - make sure `PASSWORD` is replaced with your actual password
2. Get a fresh connection string from https://console.neon.tech
3. Update `.env` and try again:
   ```bash
   python create_tables.py
   ```

### Database Connection Refused?

**Error:** `connection to server at "..." failed`

**Possible causes:**
- `.env` is using placeholder values (PASSWORD, ep-xxxx, etc)
- Neon connection string is incorrect
- Network connectivity issues

**Solution:**
```bash
# 1. Verify your .env
cat .env

# 2. Test the connection manually
psql "postgresql://neondb_owner:PASSWORD@ep-xxxx.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require"

# 3. Get fresh credentials from Neon
# Go to: https://console.neon.tech → Your Project → Connection string
```

### API won't start?

**Make sure:**
1. ✅ All dependencies installed: `pip install -r requirements.txt`
2. ✅ `.env` file exists with real database credentials
3. ✅ Database tables created: `python create_tables.py`

**Then start:**
```bash
uvicorn app.main:app --reload
```

### Events not being processed?

1. Check event loop is running: `python event_loop.py`
2. Check logs for errors (should show in terminal)
3. Verify database connection: `python create_tables.py`

## Development

### Run tests

```bash
pytest tests/
```

### Format code

```bash
black app/ event_loop.py
```

### Lint

```bash
flake8 app/ event_loop.py
```

## n8n Integration (Legacy)

If you're migrating from n8n, the API is backward compatible. The n8n workflow that sends to:

```
https://your-domain.com/66845e3b-feb9-40f1-bc83-d91eca5aea13
```

Will still work with the API.

Recommended: Update your n8n webhook to use `/events` instead.

## License

MIT

## Author

Created for hamster game project