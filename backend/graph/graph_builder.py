from langgraph.graph import StateGraph
from backend.graph.state import CoachState

from backend.graph.nodes import (
    profile_node,
    analytics_node,
    recommendation_node,
    coach_summary_node
)

builder = StateGraph(CoachState)

builder.add_node("profile",profile_node)
builder.add_node("analytics",analytics_node)
builder.add_node("recommendations", recommendation_node)
builder.add_node("coach summary",coach_summary_node)
builder.set_entry_point("profile")

builder.add_edge( "profile", "analytics")
builder.add_edge( "analytics", "recommendations")
builder.add_edge( "recommendations","coach summary")
graph = builder.compile()
result = graph.invoke(
    {
        "handle": "tourist"
    }
)

print(result)