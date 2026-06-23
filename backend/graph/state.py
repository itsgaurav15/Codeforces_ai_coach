from typing import TypedDict


class CoachState(TypedDict):
    handle: str
    profile: dict
    analytics: dict
    recommendations: list
    summary: str