from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Normalize database URL for async SQLAlchemy.
# If user supplies postgresql://, convert to postgresql+asyncpg://
raw_url = settings.database_url.strip()
parsed_url = make_url(raw_url)

if parsed_url.drivername == "postgresql":
    engine_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    engine_url = raw_url

# asyncpg does not accept sslmode/channel_binding directly as kwargs.
# Use `ssl=True` and remove unsupported query params from the URL.
query = dict(parsed_url.query)
connect_args = {}

if query.pop("sslmode", None) is not None:
    connect_args["ssl"] = True

if query.pop("channel_binding", None) is not None:
    # channel_binding is not passed directly to asyncpg. If TLS is enabled,
    # asyncpg will negotiate channel binding automatically when supported.
    connect_args.setdefault("ssl", True)

# Rebuild the URL without unsupported query args.
base_engine_url = engine_url.split("?", 1)[0]
if query:
    query_parts = [f"{key}={value}" for key, value in query.items()]
    engine_url = f"{base_engine_url}?{'&'.join(query_parts)}"
else:
    engine_url = base_engine_url

# Create async database engine
engine = create_async_engine(
    engine_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True,
    connect_args=connect_args if connect_args else None,
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session() as session:
        yield session


async def init_db():
    """Initialize database - create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

