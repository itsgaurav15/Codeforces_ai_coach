from fastapi import APIRouter
from backend.services.codeforces_service import get_user_info
from backend.services.submission_service import sync_submissions
from backend.services.analytics import analytics_report
from backend.services.problem_service import sync_problems
from backend.services.recommendation_service import (
    recommend_problems
)
from backend.graph.graph_builder import graph
from backend.services.planner_service import generate_practice_plan
from backend.services.contest_service import contest_analysis
from backend.services.contest_sync_service import sync_contests

router = APIRouter()

@router.get("/profile/{handle}")
def profile(handle: str):
    return get_user_info(handle)

@router.get("/sync-submissions/{handle}")
def sync(handle: str):
    return sync_submissions(handle)

@router.get("/analytics/{handle}")
def analytics(handle: str):

    return analytics_report(handle)

@router.get("/sync-problems")
def sync():
    return sync_problems()


@router.get("/recommendations/{handle}")
def recommendations(handle: str):

    return recommend_problems(handle)


@router.get("/coach/{handle}")
def coach(handle:str):
    result=graph.invoke(
        {
            "handle":handle
        }
    )
    return result

@router.get("/plan/{handle}")
def plan(handle:str):
    return generate_practice_plan(handle)

@router.get("/contest-analysis/{handle}")
def contest(handle):

    return contest_analysis(handle)

@router.get("/sync-contests/{handle}")
def contest_sync(handle: str):

    return sync_contests(handle)