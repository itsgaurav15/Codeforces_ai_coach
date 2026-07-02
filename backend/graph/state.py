from typing import TypedDict


class CoachState(TypedDict):
    handle: str
    profile: dict
    analytics: dict
    recommendations: list
    practice_plan:dict
    contest_analysis:dict
    summary: str