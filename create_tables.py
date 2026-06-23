from backend.database import engine

from backend.models.base import Base
from backend.models.user import User
from backend.models.submission import Submission
from backend.models.problem import Problem
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")