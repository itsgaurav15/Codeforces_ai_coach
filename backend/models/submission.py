from sqlalchemy import Column, Integer, String
from backend.models.base import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    handle = Column(String, nullable=False, index=True)

    contest_id = Column(Integer)

    problem_name = Column(String)

    problem_index = Column(String)

    verdict = Column(String)

    rating = Column(Integer)

    tags = Column(String)

    programming_language = Column(String)