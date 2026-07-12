from sqlalchemy import Column, Integer, String
from backend.models.base import Base


class Contest(Base):

    __tablename__ = "contests"

    id = Column(Integer, primary_key=True)

    handle = Column(String, index=True)

    contest_id = Column(Integer)

    contest_name = Column(String)

    rank = Column(Integer)

    old_rating = Column(Integer)

    new_rating = Column(Integer)

    rating_change = Column(Integer)

    contest_time = Column(Integer)