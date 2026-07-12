import logging

from backend.services.codeforces_service import get_user_info
from backend.services.analytics import analytics_report
from backend.services.recommendation_service import recommend_problems
from backend.services.planner_service import generate_practice_plan
from backend.services.contest_service import contest_analysis 
from backend.prompts.coach_prompts import build_coach_prompt
from backend.services.llm_service import ask_coach

logger = logging.getLogger(__name__)

def profile_node(state):

    handle = state["handle"]

    return {
        "profile": get_user_info(handle)
    }

def analytics_node(state):

    handle = state["handle"]

    report = analytics_report(handle)

    return {
        "analytics": report,
        # Cache weak tags in state so downstream nodes don't recompute them.
        "weak_tags": [
            topic["tag"]
            for topic in report.get("weak_topics", [])
        ],
    }

def recommendation_node(state):

    handle = state["handle"]

    return {
        "recommendations": recommend_problems(
            handle,
            state.get("weak_tags"),
        )
    }


def coach_summary_node(state):

    prompt = build_coach_prompt(state)

    advice = ask_coach(prompt)

    return {
        "summary": advice
    }

def planner_node(state):

    handle = state["handle"]

    return {
        "practice_plan": generate_practice_plan(
            handle,
            state.get("weak_tags"),
            state.get("recommendations"),
        )
    }

def contest_node(state):

    result = contest_analysis(state["handle"])

    logger.debug("Contest Analysis: %s", result)

    return {
        "contest_analysis": result
    }