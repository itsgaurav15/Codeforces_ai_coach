from backend.services.codeforces_service import get_user_info
from backend.services.analytics import analytics_report
from backend.services.recommendation_service import recommend_problems

def profile_node(state):

    handle = state["handle"]

    state["profile"] = get_user_info(handle)

    return state

def analytics_node(state):

    handle = state["handle"]

    state["analytics"] = analytics_report(handle)

    return state

def recommendation_node(state):

    handle = state["handle"]

    state["recommendations"] = recommend_problems(handle)

    return state

def coach_summary_node(state):

    weak = state["analytics"]["weak_topics"]

    recs = state["recommendations"]

    summary = f"""
Current Rating: {state['profile'].get('rating')}

Weak Topics:
{[x['tag'] for x in weak]}

Recommended Problems:
{[x['name'] for x in recs[:5]]}
"""

    state["summary"] = summary

    return state