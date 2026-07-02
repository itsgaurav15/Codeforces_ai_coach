from langgraph.graph import StateGraph, END

from backend.graph.state import CoachState

from backend.graph.nodes import (
    profile_node,
    analytics_node,
    contest_node,
    recommendation_node,
    planner_node,
    coach_summary_node,
)

builder = StateGraph(CoachState)

builder.add_node("profile", profile_node)
builder.add_node("analytics", analytics_node)
builder.add_node("contest", contest_node)
builder.add_node("recommendation", recommendation_node)
builder.add_node("planner", planner_node)
builder.add_node("coach", coach_summary_node)

builder.set_entry_point("profile")

builder.add_edge("profile", "analytics")
builder.add_edge("analytics", "contest")
builder.add_edge("contest", "recommendation")
builder.add_edge("recommendation", "planner")
builder.add_edge("planner", "coach")
builder.add_edge("coach", END)

graph = builder.compile()