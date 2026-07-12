from sqlalchemy import Column, Integer, String, UniqueConstraint
from backend.models.base import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)

    contest_id = Column(Integer)

    problem_index = Column(String)

    name = Column(String)

    rating = Column(Integer, index=True)

    tags = Column(String)

    # A problem is uniquely identified by (contest_id, index) on Codeforces
    # — e.g. contest 1500, problem "A". This lets sync_problems() tell new
    # problems apart from ones it already has, instead of wiping the whole
    # table every sync.
    __table_args__ = (
        UniqueConstraint("contest_id", "problem_index", name="uq_problem_key"),
    )
