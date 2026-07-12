from typing import TypedDict


class CoachState(TypedDict):
    handle: str
    profile: dict
    analytics: dict
    weak_tags: list
    recommendations: list
    practice_plan:dict
    contest_analysis:dict
    summary: str