"""Pydantic response schemas.

Wiring these into route `response_model=` gives us three things for free:
1. FastAPI validates the response shape before it goes out (catches bugs
   where a service starts returning a differently-shaped dict).
2. The auto-generated OpenAPI docs (/docs) show a real, typed schema
   instead of "any object".
3. Frontend/consumer code has a single source of truth for the contract.
"""

from typing import Optional

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    handle: str
    rating: Optional[int] = None
    maxRating: Optional[int] = None
    rank: Optional[str] = None
    maxRank: Optional[str] = None
    country: Optional[str] = None
    organization: Optional[str] = None
    titlePhoto: Optional[str] = None


class TopicStat(BaseModel):
    tag: str
    success_rate: float


class AnalyticsResponse(BaseModel):
    overall_success_rate: float
    weak_topics: list[TopicStat]
    strong_topics: list[TopicStat]
