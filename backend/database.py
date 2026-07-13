import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# In production (Render/Railway/etc.) DATABASE_URL will point at a managed
# Postgres instance. Locally, it falls back to the SQLite file so nothing
# breaks for local development.
_raw_database_url = os.getenv("DATABASE_URL")

if _raw_database_url is not None and _raw_database_url.strip() == "":
    # The env var exists but is blank — os.getenv's default only applies
    # when the key is entirely absent, so this would otherwise silently
    # reach create_engine("") and fail with a cryptic
    # "Could not parse SQLAlchemy URL" error with no indication why.
    raise RuntimeError(
        "DATABASE_URL is set but empty. Either remove the environment "
        "variable entirely (to fall back to local SQLite), or set it to "
        "your Postgres connection string (no surrounding quotes)."
    )

DATABASE_URL = (_raw_database_url or "sqlite:///coach.db").strip().strip('"').strip("'")

# Render/Railway sometimes hand back "postgres://" which SQLAlchemy 2.x
# rejects — it wants "postgresql://".
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
