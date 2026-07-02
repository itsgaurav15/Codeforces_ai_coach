from fastmcp import FastMCP
from tools import (
    coach,
    profile,
    analytics,
    recommendations,
    contest_analysis,
    practice_plan
)

mcp = FastMCP("Codeforces AI Coach")


@mcp.tool
async def get_profile(handle: str):
    """Fetch Codeforces profile."""
    return await profile(handle)


@mcp.tool
async def get_analytics(handle: str):
    """Fetch analytics."""
    return await analytics(handle)


@mcp.tool
async def get_recommendations(handle: str):
    """Fetch recommended problems."""
    return await recommendations(handle)


@mcp.tool
async def get_contest_analysis(handle: str):
    """Fetch contest analysis."""
    return await contest_analysis(handle)


@mcp.tool
async def get_practice_plan(handle: str):
    """Fetch practice plan."""
    return await practice_plan(handle)


@mcp.tool
async def get_coach(handle: str):
    """Run the complete AI Coach."""
    return await coach(handle)


if __name__ == "__main__":
    print("Starting Codeforces AI Coach MCP Server...")
    mcp.run()