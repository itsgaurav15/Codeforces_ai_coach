import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# In production (Render/Railway/etc.) DATABASE_URL will point at a managed
# Postgres instance. Locally, it falls back to the SQLite file so nothing
# breaks for local development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///coach.db")

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
