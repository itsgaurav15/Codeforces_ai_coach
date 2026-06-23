from sqlalchemy import Column, Integer, String

from backend.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    handle = Column(String)

    rating = Column(Integer)

    max_rating = Column(Integer)