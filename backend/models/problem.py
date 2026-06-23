from sqlalchemy import Column, Integer, String
from backend.models.base import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)

    contest_id = Column(Integer)

    problem_index = Column(String)

    name = Column(String)

    rating = Column(Integer)

    tags = Column(String)