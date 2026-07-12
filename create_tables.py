"""One-off manual table creation.

NOTE: This is no longer required for normal operation. backend/main.py's
`lifespan` handler now calls Base.metadata.create_all() automatically on
every server startup (idempotent — safe to run repeatedly).

This script is kept only as a convenience for creating tables without
spinning up the full server, e.g. in a one-off shell or CI step:

    python create_tables.py
"""

from backend.database import engine

from backend.models.base import Base
from backend.models.user import User
from backend.models.submission import Submission
from backend.models.problem import Problem
from backend.models.contest import Contest

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
