import httpx

from config import FASTAPI_URL

# Reuse a single client instead of opening a new connection for every call.
_client = httpx.AsyncClient(base_url=FASTAPI_URL, timeout=120)


async def call(endpoint: str):

    response = await _client.get(f"/{endpoint}")

    response.raise_for_status()

    return response.json()


async def coach(handle: str):
    """Runs the full LangGraph pipeline, including the LLM coaching
    summary. Only use this when the LLM-generated summary is actually
    needed — it's far more expensive than the endpoints below."""

    return await call(
        f"coach/{handle}"
    )


async def profile(handle: str):

    return await call(
        f"profile/{handle}"
    )


async def analytics(handle: str):

    return await call(
        f"analytics/{handle}"
    )


async def recommendations(handle: str):
    # Hits the dedicated endpoint directly instead of running the whole
    # coach pipeline (and paying for an LLM call) just for this list.
    return await call(
        f"recommendations/{handle}"
    )


async def contest_analysis(handle: str):
    return await call(
        f"contest-analysis/{handle}"
    )


async def practice_plan(handle: str):
    return await call(
        f"plan/{handle}"
    )