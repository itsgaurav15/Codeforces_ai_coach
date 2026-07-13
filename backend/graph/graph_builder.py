from langgraph.graph import StateGraph, END

from backend.graph.state import CoachState

from backend.graph.nodes import (
    sync_node,
    profile_node,
    analytics_node,
    contest_node,
    recommendation_node,
    planner_node,
    coach_summary_node,
)

builder = StateGraph(CoachState)

builder.add_node("sync", sync_node)
builder.add_node("profile_", profile_node)
builder.add_node("analytics_", analytics_node)
builder.add_node("contest", contest_node)
builder.add_node("recommendation", recommendation_node)
builder.add_node("planner", planner_node)
builder.add_node("coach", coach_summary_node)

builder.set_entry_point("sync")

builder.add_edge("sync", "profile_")
builder.add_edge("profile_", "analytics_")
builder.add_edge("analytics_", "contest")
builder.add_edge("contest", "recommendation")
builder.add_edge("recommendation", "planner")
builder.add_edge("planner", "coach")
builder.add_edge("coach", END)

graph = builder.compile()
